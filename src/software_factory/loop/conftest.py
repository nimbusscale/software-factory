import asyncio
import shutil
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest

from software_factory.conftest import commit_file, run_git
from software_factory.git.working_copy import Remote
from software_factory.github.fake_github import REPO, FakeGitHub, FakeIssue
from software_factory.loop.run import RunRequest, Services, run
from software_factory.roles.fake_agent_sdk import ScriptedQuery, result_message
from software_factory.roles.run import RoleRunner

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from pathlib import Path

    from pydantic import JsonValue

    from software_factory.github.pull_request import PullRequest
    from software_factory.roles.fake_agent_sdk import RawMessage, Turn

ISSUE_NUMBER = 7
ISSUE_BODY = "## Why\n\nThe game needs tiles.\n"
STARTED = datetime(2026, 11, 24, 21, 30, 0, tzinfo=UTC)
RUN_BRANCH = "factory/issue-7-20261124-213000"
IMPLEMENTER_SESSION = "implementer-session"
FACTORY_VERSION = "0123456789ab"


def fake_github() -> FakeGitHub:
    issue = FakeIssue(number=ISSUE_NUMBER, title="Add the tiles", body=ISSUE_BODY)
    return FakeGitHub(issues=[issue])


def implementer_turn(
    files: Mapping[str, str],
    commit_message: str,
    declined: Sequence[tuple[str, str]] = (),
) -> Turn:
    """The implementer writes `files`, and hands back a result.

    `declined` holds the ID of each finding it declines, and the reason.
    """

    def turn(cwd: Path) -> list[RawMessage]:
        for name, text in files.items():
            (cwd / name).write_text(text)
        result: dict[str, JsonValue] = {
            "summary": "Adds the tiles.",
            "declined": [
                {"finding_id": finding_id, "reason": reason}
                for finding_id, reason in declined
            ],
            "disagreements": [],
            "decisions": [],
            "missing_reasons": [],
            "commit_message": commit_message,
        }
        return [
            result_message(structured_output=result, session_id=IMPLEMENTER_SESSION)
        ]

    return turn


def finding(mark: str, problem: str) -> JsonValue:
    return {
        "file": "TILES.md",
        "line": 1,
        "label": "F1",
        "mark": mark,
        "problem": problem,
        "failure_case": "A game with no tiles.",
        "label_reason": "It breaks normal use.",
    }


@dataclass
class SeenReviewCopies:
    """A copy of each review copy a reviewer ran in, since the run removes them."""

    folder: Path
    copies: list[Path] = field(default_factory=list)


def reviewer_turn(
    findings: Sequence[JsonValue], seen: SeenReviewCopies | None = None
) -> Turn:
    """The quality reviewer hands back `findings`."""

    def turn(cwd: Path) -> list[RawMessage]:
        if seen is not None:
            kept = seen.folder / f"review-{len(seen.copies) + 1}"
            shutil.copytree(cwd, kept, symlinks=True)
            seen.copies.append(kept)
        result: dict[str, JsonValue] = {
            "status": "done",
            "reason": f"{len(findings)} findings, and 0 dropped.",
            "findings": list(findings),
            "dropped": [],
        }
        return [result_message(structured_output=result, session_id=str(cwd))]

    return turn


# A Makefile whose targets each pass, and do nothing.
PASSING_MAKEFILE = "setup:\n\t@true\n\ncheck:\n\t@true\n"


@pytest.fixture
def author(author: Path) -> Path:
    """The author's clone, of a project that meets the project contract."""
    push_files(
        author,
        {
            "Makefile": PASSING_MAKEFILE,
            "docs/functional-spec.md": "# Functional spec\n",
            "docs/technical-spec.md": "# Technical spec\n",
        },
    )
    return author


def push_files(author: Path, files: Mapping[str, str]) -> None:
    """Puts `files` on the project's default branch, in one commit."""
    for name, text in files.items():
        (author / name).parent.mkdir(parents=True, exist_ok=True)
        (author / name).write_text(text)
    run_git("add", "--all", cwd=author)
    run_git("commit", "--quiet", "--message", "Change the project", cwd=author)
    run_git("push", "--quiet", "origin", "main", cwd=author)


def push_settings(author: Path, text: str) -> None:
    """Puts a settings file on the project's default branch."""
    commit_file(author, "software-factory.toml", text)
    run_git("push", "--quiet", "origin", "main", cwd=author)


def services(
    github: FakeGitHub,
    roles: ScriptedQuery,
    remote: Path,
    home: Path,
) -> Services:
    return Services(
        graphql=github,
        runner=RoleRunner(roles),
        home=home,
        remote=lambda repo: Remote(str(remote) if repo == REPO else ""),
        factory_version=FACTORY_VERSION,
    )


def start_run(services: Services, rounds: int | None = None) -> PullRequest:
    request = RunRequest(
        repo=REPO, issue_number=ISSUE_NUMBER, rounds=rounds, started_at=STARTED
    )
    return asyncio.run(run(request, services))


def board_status(github: FakeGitHub) -> str | None:
    return github.board.status_of(github.issue(ISSUE_NUMBER))
