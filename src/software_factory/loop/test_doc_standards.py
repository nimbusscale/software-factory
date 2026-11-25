"""Runs that give their roles the factory's doc standards."""

from typing import TYPE_CHECKING

import pytest

from software_factory.conftest import (
    FACTORY_STANDARDS,
    commit_files,
    make_factory_remote,
    run_git,
)
from software_factory.loop.conftest import (
    RUN_BRANCH,
    fake_github,
    finding,
    implementer_turn,
    reviewer_turn,
    services,
    start_run,
)
from software_factory.loop.run import RunRefusedError
from software_factory.roles.fake_agent_sdk import ScriptedQuery

if TYPE_CHECKING:
    from pathlib import Path

    from software_factory.roles.fake_agent_sdk import RawMessage, Turn

PROJECT_STANDARDS = {
    "docs/standards/README.md": "The project's own standards.\n",
    "docs/standards/review-rubric.md": "The project's own rubric.\n",
    "tools/check-docs.sh": "echo The project's check\n",
}


def reading(seen: list[dict[str, str]], turn: Turn) -> Turn:
    """`turn`, after it keeps the doc standards in the folder the role runs in."""

    def read_then_turn(cwd: Path) -> list[RawMessage]:
        seen.append({name: (cwd / name).read_text() for name in FACTORY_STANDARDS})
        return turn(cwd)

    return read_then_turn


def run_changes(remote: Path) -> list[str]:
    changed = run_git("diff", "--name-only", f"main...{RUN_BRANCH}", cwd=remote)
    return changed.splitlines()


def factory_main(tmp_path: Path) -> str:
    return run_git("rev-parse", "main", cwd=make_factory_remote(tmp_path))


def test_project_with_no_standards_gets_the_factorys(
    remote: Path, tmp_path: Path
) -> None:
    seen: list[dict[str, str]] = []
    roles = ScriptedQuery(
        [
            reading(seen, implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles")),
            reading(seen, reviewer_turn([])),
        ]
    )
    github = fake_github()

    start_run(services(github, roles, remote, tmp_path / "home"))

    assert seen == [FACTORY_STANDARDS, FACTORY_STANDARDS]
    # FR-36.
    assert run_changes(remote) == ["TILES.md"]
    # FR-37.
    [opened] = github.pull_requests
    commit = factory_main(tmp_path)
    assert f"nimbusscale/software-factory@{commit}." in opened.body


def test_project_with_its_own_standards_gets_the_factorys(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    """Meets FR-32 and FR-36."""
    commit_files(author, PROJECT_STANDARDS, "Add the project's standards")
    run_git("push", "--quiet", "origin", "main", cwd=author)
    seen: list[dict[str, str]] = []
    roles = ScriptedQuery(
        [
            reading(seen, implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles")),
            reading(seen, reviewer_turn([])),
        ]
    )

    start_run(services(fake_github(), roles, remote, tmp_path / "home"))

    assert seen == [FACTORY_STANDARDS, FACTORY_STANDARDS]
    assert run_changes(remote) == ["TILES.md"]


def test_implementers_change_to_the_standards_is_undone(
    remote: Path, tmp_path: Path
) -> None:
    """Meets FR-35 and FR-36, for a change the edit guard's hook can't see."""
    changed = {"TILES.md": "Tiles\n", "docs/standards/README.md": "Changed.\n"}
    seen: list[dict[str, str]] = []
    roles = ScriptedQuery(
        [
            implementer_turn(changed, "Add the tiles"),
            reading(seen, reviewer_turn([finding("important", "No deal.")])),
            reading(seen, implementer_turn({"TILES.md": "Dealt\n"}, "Deal them")),
            reading(seen, reviewer_turn([])),
        ]
    )

    start_run(services(fake_github(), roles, remote, tmp_path / "home"), rounds=2)

    assert seen == [FACTORY_STANDARDS] * 3
    assert run_changes(remote) == ["TILES.md"]


def test_branch_the_command_names_gives_the_standards(
    remote: Path, tmp_path: Path
) -> None:
    """Meets FR-33."""
    factory_author = make_factory_remote(tmp_path).parent / "factory-author"
    trial = {"docs/standards/README.md": "Trial standards.\n"}
    run_git("switch", "--quiet", "-c", "trial", cwd=factory_author)
    trial_commit = commit_files(factory_author, trial, "Try new standards")
    run_git("push", "--quiet", "origin", "trial", cwd=factory_author)
    seen: list[dict[str, str]] = []
    roles = ScriptedQuery(
        [
            reading(seen, implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles")),
            reading(seen, reviewer_turn([])),
        ]
    )
    github = fake_github()

    start_run(services(github, roles, remote, tmp_path / "home"), standards="trial")

    assert seen == [FACTORY_STANDARDS | trial] * 2
    [opened] = github.pull_requests
    assert f"nimbusscale/software-factory@{trial_commit}." in opened.body


def test_branch_that_doesnt_exist_refuses_the_run(remote: Path, tmp_path: Path) -> None:
    """Meets FR-34."""
    github = fake_github()

    with pytest.raises(RunRefusedError, match="has no branch missing"):
        start_run(
            services(github, ScriptedQuery([]), remote, tmp_path / "home"),
            standards="missing",
        )

    assert github.operations == []
