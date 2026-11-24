import asyncio
from datetime import UTC, datetime, timedelta, timezone
from typing import TYPE_CHECKING

import pytest

from software_factory.git.command import CommitId, git
from software_factory.git.conftest import commit_file, run_git
from software_factory.git.working_copy import (
    Clone,
    WorkingCopy,
    commit,
    open_clone,
    push,
    run_branch_name,
    working_copy,
)

if TYPE_CHECKING:
    from pathlib import Path

ISSUE = 7
STARTED = datetime(2026, 11, 24, 21, 30, 0, tzinfo=UTC)
RUN_BRANCH = "factory/issue-7-20261124-213000"


def clone_of(remote: Path) -> Clone:
    return asyncio.run(open_clone(str(remote), remote.parent / "clones" / "dust-law"))


def tip(repo: Path, ref: str) -> CommitId:
    return CommitId(run_git("rev-parse", ref, cwd=repo))


async def start_and_end_run(clone: Clone, path: Path) -> WorkingCopy:
    async with working_copy(clone, ISSUE, STARTED, path) as copy:
        return copy


def test_first_run_makes_the_clone(remote: Path, author: Path) -> None:
    clone = clone_of(remote)

    assert tip(clone.path, "origin/main") == tip(author, "HEAD")


def test_later_run_fetches_into_the_clone(remote: Path, author: Path) -> None:
    clone_of(remote)
    new_commit = commit_file(author, "RULES.md", "Rules\n")
    run_git("push", "--quiet", "origin", "main", cwd=author)

    clone = clone_of(remote)

    assert tip(clone.path, "origin/main") == new_commit


def test_run_branch_starts_from_the_default_branch(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    clone = clone_of(remote)

    copy = asyncio.run(start_and_end_run(clone, tmp_path / "work"))

    assert copy.run_branch == RUN_BRANCH
    assert copy.start == tip(author, "HEAD")
    assert tip(clone.path, copy.run_branch) == copy.start


def test_run_branch_follows_a_change_of_default_branch(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    clone_of(remote)
    run_git("switch", "--quiet", "--create", "trunk", cwd=author)
    trunk = commit_file(author, "RULES.md", "Rules\n")
    run_git("push", "--quiet", "origin", "trunk", cwd=author)
    run_git("symbolic-ref", "HEAD", "refs/heads/trunk", cwd=remote)

    copy = asyncio.run(start_and_end_run(clone_of(remote), tmp_path / "work"))

    assert copy.start == trunk


def test_run_branch_name_holds_the_start_time_in_utc() -> None:
    eastern = timezone(timedelta(hours=-5))

    name = run_branch_name(ISSUE, datetime(2026, 11, 24, 16, 30, 0, tzinfo=eastern))

    assert name == RUN_BRANCH


def test_earlier_run_branch_is_kept(remote: Path, tmp_path: Path) -> None:
    clone = clone_of(remote)

    async def earlier_run() -> CommitId | None:
        async with working_copy(clone, ISSUE, STARTED, tmp_path / "earlier") as copy:
            (copy.path / "TILES.md").write_text("Tiles\n")
            return await commit(copy, "Add the tiles")

    earlier_commit = asyncio.run(earlier_run())

    async def later_run() -> WorkingCopy:
        later = STARTED + timedelta(minutes=5)
        async with working_copy(clone, ISSUE, later, tmp_path / "later") as copy:
            return copy

    copy = asyncio.run(later_run())

    assert copy.run_branch == "factory/issue-7-20261124-213500"
    assert tip(clone.path, copy.run_branch) == copy.start
    assert tip(clone.path, RUN_BRANCH) == earlier_commit


class RunFailedError(Exception):
    pass


def test_run_end_removes_the_working_copy_and_keeps_the_branch(
    remote: Path, tmp_path: Path
) -> None:
    clone = clone_of(remote)
    committed: list[CommitId | None] = []

    async def run_that_fails() -> None:
        async with working_copy(clone, ISSUE, STARTED, tmp_path / "work") as copy:
            (copy.path / "TILES.md").write_text("Tiles\n")
            committed.append(await commit(copy, "Add the tiles"))
            (copy.path / "RULES.md").write_text("Not committed\n")
            raise RunFailedError

    with pytest.raises(RunFailedError):
        asyncio.run(run_that_fails())

    assert not (tmp_path / "work").exists()
    assert committed == [tip(clone.path, RUN_BRANCH)]


def test_commit_holds_every_change_with_the_given_message(
    remote: Path, tmp_path: Path
) -> None:
    clone = clone_of(remote)

    async def run() -> tuple[WorkingCopy, CommitId | None]:
        async with working_copy(clone, ISSUE, STARTED, tmp_path / "work") as copy:
            (copy.path / "README.md").unlink()
            (copy.path / "rules").mkdir()
            (copy.path / "rules" / "RULES.md").write_text("Rules\n")
            return copy, await commit(copy, "Move the readme to the rules")

    copy, committed = asyncio.run(run())

    assert committed == tip(clone.path, copy.run_branch)
    files = run_git("ls-tree", "-r", "--name-only", copy.run_branch, cwd=clone.path)
    assert files.splitlines() == ["rules/RULES.md"]
    message = run_git("log", "-1", "--format=%B", copy.run_branch, cwd=clone.path)
    assert message == "Move the readme to the rules"


def test_commit_with_no_changes_hands_back_none(remote: Path, tmp_path: Path) -> None:
    clone = clone_of(remote)

    async def run() -> CommitId | None:
        async with working_copy(clone, ISSUE, STARTED, tmp_path / "work") as copy:
            return await commit(copy, "Nothing")

    assert asyncio.run(run()) is None


def test_commit_with_changes_only_inside_a_submodule_hands_back_none(
    remote: Path, tmp_path: Path
) -> None:
    library = tmp_path / "library"
    library.mkdir()
    run_git("init", "--quiet", cwd=library)
    commit_file(library, "tiles.py", "TILES = []\n")
    clone = clone_of(remote)

    async def run() -> CommitId | None:
        async with working_copy(clone, ISSUE, STARTED, tmp_path / "work") as copy:
            add = ("-c", "protocol.file.allow=always", "submodule", "add", "--quiet")
            await git(*add, str(library), "lib", cwd=copy.path)
            await commit(copy, "Add the library")
            (copy.path / "lib" / "tiles.py").write_text("TILES = [1]\n")
            return await commit(copy, "Change the library")

    assert asyncio.run(run()) is None


def test_push_puts_the_run_branch_on_the_remote(remote: Path, tmp_path: Path) -> None:
    clone = clone_of(remote)

    async def run() -> CommitId | None:
        async with working_copy(clone, ISSUE, STARTED, tmp_path / "work") as copy:
            (copy.path / "TILES.md").write_text("Tiles\n")
            committed = await commit(copy, "Add the tiles")
            await push(copy)
            return committed

    committed = asyncio.run(run())

    assert tip(remote, RUN_BRANCH) == committed
