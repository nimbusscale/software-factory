import asyncio
from typing import TYPE_CHECKING

import pytest

from software_factory.conftest import run_git
from software_factory.git.working_copy import Remote
from software_factory.github.fake_github import (
    REPO,
    FakeGitHub,
    FakeIssue,
    FakePullRequest,
)
from software_factory.loop.conftest import (
    ISSUE_BODY,
    ISSUE_NUMBER,
    SeenReviewCopies,
    finding,
    push_files,
    reviewer_turn,
)
from software_factory.review.review import (
    NOTHING_TO_FIX,
    Review,
    ReviewEndedError,
    ReviewRequest,
    ReviewServices,
    review_pull_request,
)
from software_factory.roles.fake_agent_sdk import ScriptedQuery, result_message
from software_factory.roles.run import RoleRunner

if TYPE_CHECKING:
    from pathlib import Path

    from pydantic import JsonValue

    from software_factory.roles.fake_agent_sdk import RawMessage, Turn

PR_NUMBER = 5
PR_ID = f"PR_{PR_NUMBER}"
# The setup leaves a file git ignores, as a project's environment would be.
SETUP_MAKEFILE = "setup:\n\t@mkdir -p .venv && touch .venv/ready\n"
FAILING_SETUP_MAKEFILE = "setup:\n\t@echo no npm; exit 1\n"


def open_pull_request(
    author: Path, makefile: str = SETUP_MAKEFILE, closes: list[int] | None = None
) -> FakeGitHub:
    """Pushes a PR's head that adds TILES.md, and a fake GitHub that holds the PR.

    The default branch gets RULES.md after the PR's head branched off it.
    """
    push_files(author, {"Makefile": makefile, ".gitignore": ".venv/\n"})
    run_git("switch", "--quiet", "--create", "tiles", cwd=author)
    push_files_to(author, {"TILES.md": "Tiles\n"}, f"HEAD:refs/pull/{PR_NUMBER}/head")
    run_git("switch", "--quiet", "main", cwd=author)
    push_files(author, {"RULES.md": "Rules\n"})
    issues = [
        FakeIssue(number=ISSUE_NUMBER, title="Add the tiles", body=ISSUE_BODY),
        FakeIssue(number=8, title="Add the rules", body="## Why\n\nRules.\n"),
    ]
    pull_request = FakePullRequest(
        number=PR_NUMBER,
        base="main",
        head="tiles",
        title="Add the tiles",
        body="I added the tiles, and they're right.",
        closes=[ISSUE_NUMBER] if closes is None else closes,
    )
    return FakeGitHub(issues=issues, pull_requests=[pull_request])


def push_files_to(author: Path, files: dict[str, str], refspec: str) -> None:
    for name, text in files.items():
        (author / name).write_text(text)
    run_git("add", "--all", cwd=author)
    run_git("commit", "--quiet", "--message", "Change the PR", cwd=author)
    run_git("push", "--quiet", "origin", refspec, cwd=author)


def start_review(github: FakeGitHub, roles: ScriptedQuery, remote: Path) -> Review:
    services = ReviewServices(
        graphql=github,
        runner=RoleRunner(roles),
        remote=lambda repo: Remote(str(remote) if repo == REPO else ""),
        factory_version="0123456789ab",
        run_folder="20261127T120000Z-review-nimbusscale-dust-law-5",
    )
    request = ReviewRequest(repo=REPO, pull_request_number=PR_NUMBER)
    return asyncio.run(review_pull_request(request, services))


def changed_files(review_copy: Path) -> list[str]:
    return run_git("diff", "HEAD", "--name-only", cwd=review_copy).splitlines()


def test_reviews_the_prs_changes_since_it_branched_off(
    author: Path, remote: Path, tmp_path: Path
) -> None:
    seen = SeenReviewCopies(tmp_path)
    roles = ScriptedQuery([reviewer_turn([], seen)])

    start_review(open_pull_request(author), roles, remote)

    [copy] = seen.copies
    # FR-47.
    assert not roles.turns
    # TR-25.
    assert changed_files(copy) == ["TILES.md"]
    assert not (copy / "RULES.md").exists()
    # TR-23.
    assert (copy / ".venv" / "ready").exists()


def test_reviewer_gets_the_body_of_the_issue_the_pr_closes(
    author: Path, remote: Path
) -> None:
    roles = ScriptedQuery([reviewer_turn([])])

    start_review(open_pull_request(author), roles, remote)

    [prompt] = roles.prompts
    # TR-26.
    assert f"<issue>\n{ISSUE_BODY.strip()}\n</issue>" in prompt
    assert "I added the tiles" not in prompt
    assert "<earlier_findings>\nNone.\n</earlier_findings>" in prompt


@pytest.mark.parametrize("closes", [[], [ISSUE_NUMBER, 8]])
def test_reviewer_gets_no_issue_when_the_pr_doesnt_close_one(
    author: Path, remote: Path, closes: list[int]
) -> None:
    roles = ScriptedQuery([reviewer_turn([])])

    start_review(open_pull_request(author, closes=closes), roles, remote)

    [prompt] = roles.prompts
    # TR-26.
    assert "The change has no task issue." in prompt
    assert "<issue>" not in prompt


def test_prints_the_findings_the_implementer_would_get(
    author: Path, remote: Path
) -> None:
    findings = [
        finding("important", "The deal skips the last player."),
        finding("nit", "A name could be clearer."),
        finding("pre_existing", "The shuffle isn't seeded."),
    ]
    roles = ScriptedQuery([reviewer_turn(findings)])

    printed = start_review(open_pull_request(author), roles, remote).printed()

    # FR-48.
    assert "### R1-F1, an important finding" in printed
    assert "### R1-F2, a nit" in printed
    assert "The shuffle isn't seeded." not in printed


def test_prints_no_finding_without_an_important_one(author: Path, remote: Path) -> None:
    roles = ScriptedQuery([reviewer_turn([finding("nit", "A name could be clearer.")])])

    printed = start_review(open_pull_request(author), roles, remote).printed()

    # FR-48.
    assert NOTHING_TO_FIX in printed
    assert "A name could be clearer." not in printed


def reviewer_turn_with_dropped(findings: list[JsonValue]) -> Turn:
    def turn(cwd: Path) -> list[RawMessage]:
        dropped: JsonValue = {
            "file": "TILES.md",
            "line": 1,
            "problem": "The tiles could run out.",
            "label": "D1",
            "dropped_as": "false_claim",
            "reason": "The bag holds 100 tiles.",
        }
        result: dict[str, JsonValue] = {
            "status": "done",
            "reason": "Some findings, and 1 dropped.",
            "findings": findings,
            "dropped": [dropped],
        }
        return [result_message(structured_output=result, session_id=str(cwd))]

    return turn


def test_posts_the_rest_of_the_review_on_the_pr(author: Path, remote: Path) -> None:
    findings: list[JsonValue] = [
        finding("important", "The deal skips the last player."),
        finding("nit", "A name could be clearer."),
        finding("pre_existing", "The shuffle isn't seeded."),
        finding("to_check", "The scores service may refuse a draw."),
    ]
    roles = ScriptedQuery([reviewer_turn_with_dropped(findings)])
    github = open_pull_request(author)

    start_review(github, roles, remote)

    [comment] = github.comments[PR_ID]
    not_given, to_check, dropped = comment.split("## ")[1:]
    # FR-49.
    assert "R1-F3" in not_given
    assert "R1-F1" not in not_given
    assert "R1-F2" not in not_given
    assert "R1-F4" in to_check
    assert "The bag holds 100 tiles." in dropped


def test_setup_that_fails_ends_without_a_review(author: Path, remote: Path) -> None:
    roles = ScriptedQuery([reviewer_turn([])])
    github = open_pull_request(author, makefile=FAILING_SETUP_MAKEFILE)

    with pytest.raises(ReviewEndedError, match="no npm"):
        start_review(github, roles, remote)

    # TR-27.
    assert roles.turns
    assert not github.comments
