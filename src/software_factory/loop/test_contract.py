import asyncio
from typing import TYPE_CHECKING

import pytest

from software_factory.conftest import run_git
from software_factory.loop.conftest import (
    SeenReviewCopies,
    fake_github,
    implementer_turn,
    push_files,
    reviewer_turn,
    services,
    start_run,
)
from software_factory.loop.contract import ContractError, make
from software_factory.loop.run import RunRefusedError
from software_factory.roles.fake_agent_sdk import ScriptedQuery

if TYPE_CHECKING:
    from pathlib import Path


def refused_reason(remote: Path, tmp_path: Path) -> str:
    """Starts a run that should be refused, and hands back why it was."""
    github = fake_github()

    with pytest.raises(RunRefusedError) as refused:
        start_run(services(github, ScriptedQuery([]), remote, tmp_path / "home"))

    # FR-35, FR-36, FR-37: refused, so nothing but the read of the issue reached GitHub.
    assert github.operations == ["ReadIssue"]
    return str(refused.value)


@pytest.mark.parametrize(
    "spec",
    [
        ("docs/functional-spec.md", "no functional spec at `docs/functional-spec.md`"),
        ("docs/technical-spec.md", "no technical spec at `docs/technical-spec.md`"),
    ],
)
def test_project_with_a_spec_missing_refuses_the_run(
    remote: Path, author: Path, tmp_path: Path, spec: tuple[str, str]
) -> None:
    path, reason = spec
    run_git("rm", "--quiet", path, cwd=author)
    run_git("commit", "--quiet", "--message", "Remove a spec", cwd=author)
    run_git("push", "--quiet", "origin", "main", cwd=author)

    # FR-35.
    assert reason in refused_reason(remote, tmp_path)


def test_project_whose_setup_fails_refuses_the_run(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    makefile = "setup:\n\t@echo 'No package.json'; exit 1\n\ncheck:\n\t@true\n"
    push_files(author, {"Makefile": makefile})

    reason = refused_reason(remote, tmp_path)

    # FR-36.
    assert "`make setup` failed in the working copy" in reason
    assert "No package.json" in reason


def test_project_whose_checks_fail_refuses_the_run(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    makefile = "setup:\n\t@true\n\ncheck:\n\t@seq 1 40; exit 1\n"
    push_files(author, {"Makefile": makefile})

    reason = refused_reason(remote, tmp_path)

    # FR-37.
    assert "`make check` failed in the working copy" in reason
    assert "\n39\n40\nmake: ***" in reason


def test_make_the_workflow_runs_under_doesnt_reach_the_project(
    remote: Path, author: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    makefile = "setup:\n\t@true\n\ncheck:\n\t@seq 1 40; exit 1\n"
    push_files(author, {"Makefile": makefile})
    monkeypatch.setenv("MAKEFLAGS", "n")
    monkeypatch.setenv("MAKELEVEL", "1")

    reason = refused_reason(remote, tmp_path)

    # Bug: under a make started with -n, the project's failing check passed.
    assert "`make check` failed in the working copy" in reason
    assert "\n40\nmake: ***" in reason


@pytest.mark.parametrize(
    "case",
    [
        (
            "setup:\n\t@mkdir .venv; touch .venv/python\n\ncheck:\n\t@true\n",
            "`make setup` added or changed files that git doesn't ignore: `.venv/`.",
        ),
        # Bug: a path with a space or a letter outside ASCII was named the way git
        # quotes it, as "caf\303\251 notes.txt".
        (
            "setup:\n\t@touch 'café notes.txt'\n\ncheck:\n\t@true\n",
            "files that git doesn't ignore: `café notes.txt`.",
        ),
        (
            "setup:\n\t@true\n\ncheck:\n\t@echo formatted >> docs/technical-spec.md\n",
            (
                "`make check` added or changed files that git doesn't ignore:"
                " `docs/technical-spec.md`."
            ),
        ),
    ],
)
def test_target_that_leaves_files_git_doesnt_ignore_refuses_the_run(
    remote: Path, author: Path, tmp_path: Path, case: tuple[str, str]
) -> None:
    makefile, reason = case
    push_files(author, {"Makefile": makefile})

    # FR-38.
    assert reason in refused_reason(remote, tmp_path)


def test_setup_that_runs_past_its_time_limit_fails(tmp_path: Path) -> None:
    (tmp_path / "Makefile").write_text("setup:\n\t@echo Installing; sleep 30\n")

    with pytest.raises(ContractError) as failed:
        asyncio.run(make("setup", tmp_path, "the working copy", time_limit=0.5))

    # FR-36.
    assert "ran past its time limit" in str(failed.value)
    assert "Installing" in str(failed.value)


def test_make_targets_get_no_github_token(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GH_TOKEN", "github-token")
    monkeypatch.setenv("GITHUB_TOKEN", "github-token")
    (tmp_path / "Makefile").write_text("check:\n\t@env > environment\n")

    asyncio.run(make("check", tmp_path, "the working copy"))

    # AD-7.
    assert "github-token" not in (tmp_path / "environment").read_text()


def test_review_copy_holds_the_environment_setup_builds(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    makefile = "setup:\n\t@echo built > environment\n\ncheck:\n\t@test -f environment\n"
    push_files(author, {"Makefile": makefile, ".gitignore": "environment\n"})
    seen = SeenReviewCopies(tmp_path / "seen")
    seen.folder.mkdir()
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_turn([], seen),
        ]
    )

    start_run(services(fake_github(), roles, remote, tmp_path / "home"))

    [review_copy] = seen.copies
    # TR-23.
    assert (review_copy / "environment").read_text() == "built\n"
