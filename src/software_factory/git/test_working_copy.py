import asyncio
from datetime import UTC, datetime, timedelta, timezone
from typing import TYPE_CHECKING

import pytest

from software_factory.conftest import commit_file, run_git
from software_factory.git.command import CommitId, git
from software_factory.git.working_copy import (
    Remote,
    WorkingCopy,
    commit,
    head,
    push,
    run_branch_name,
    working_copy,
)

if TYPE_CHECKING:
    from contextlib import AbstractAsyncContextManager
    from pathlib import Path

ISSUE = 7
STARTED = datetime(2026, 11, 24, 21, 30, 0, tzinfo=UTC)
RUN_BRANCH = "factory/issue-7-20261124-213000"


def started(
    remote: Path, path: Path, at: datetime = STARTED
) -> AbstractAsyncContextManager[WorkingCopy]:
    return working_copy(Remote(str(remote)), ISSUE, at, path)


def tip(repo: Path, ref: str) -> CommitId:
    return CommitId(run_git("rev-parse", ref, cwd=repo))


def test_run_branch_starts_from_the_default_branch(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    async def run() -> tuple[WorkingCopy, str]:
        async with started(remote, tmp_path / "work") as copy:
            return copy, await git("branch", "--show-current", cwd=copy.path)

    copy, branch = asyncio.run(run())

    # TR-16.
    assert copy.run_branch == branch == RUN_BRANCH
    # TR-3.
    assert copy.start == tip(author, "HEAD")


def test_run_branch_name_holds_the_start_time_in_utc() -> None:
    eastern = timezone(timedelta(hours=-5))

    name = run_branch_name(ISSUE, datetime(2026, 11, 24, 16, 30, 0, tzinfo=eastern))

    assert name == RUN_BRANCH


def test_later_run_leaves_an_earlier_run_branch_as_it_is(
    remote: Path, tmp_path: Path
) -> None:
    async def earlier_run() -> CommitId | None:
        async with started(remote, tmp_path / "earlier") as copy:
            (copy.path / "TILES.md").write_text("Tiles\n")
            committed = await commit(copy, "Add the tiles")
            await push(copy)
            return committed

    earlier_commit = asyncio.run(earlier_run())

    async def later_run() -> WorkingCopy:
        later = STARTED + timedelta(minutes=5)
        async with started(remote, tmp_path / "later", later) as copy:
            await push(copy)
            return copy

    copy = asyncio.run(later_run())

    # TR-16.
    assert copy.run_branch == "factory/issue-7-20261124-213500"
    assert tip(remote, copy.run_branch) == copy.start
    assert tip(remote, RUN_BRANCH) == earlier_commit


class RunFailedError(Exception):
    pass


def test_run_end_removes_the_working_copy(remote: Path, tmp_path: Path) -> None:
    async def run_that_fails() -> None:
        async with started(remote, tmp_path / "work") as copy:
            (copy.path / "TILES.md").write_text("Tiles\n")
            await commit(copy, "Add the tiles")
            (copy.path / "RULES.md").write_text("Not committed\n")
            raise RunFailedError

    with pytest.raises(RunFailedError):
        asyncio.run(run_that_fails())

    # TR-8.
    assert not (tmp_path / "work").exists()


def test_commit_holds_every_change_with_the_given_message(
    remote: Path, tmp_path: Path
) -> None:
    async def run() -> tuple[CommitId | None, CommitId, str, str]:
        async with started(remote, tmp_path / "work") as copy:
            (copy.path / "README.md").unlink()
            (copy.path / "rules").mkdir()
            (copy.path / "rules" / "RULES.md").write_text("Rules\n")
            committed = await commit(copy, "Move the readme to the rules")
            files = await git("ls-tree", "-r", "--name-only", "HEAD", cwd=copy.path)
            message = await git("log", "-1", "--format=%B", cwd=copy.path)
            return committed, await head(copy), files, message

    committed, branch_tip, files, message = asyncio.run(run())

    # TD-7, TD-9.
    assert committed == branch_tip
    assert files.splitlines() == ["rules/RULES.md"]
    assert message == "Move the readme to the rules"


def test_commit_with_no_changes_hands_back_none(remote: Path, tmp_path: Path) -> None:
    async def run() -> CommitId | None:
        async with started(remote, tmp_path / "work") as copy:
            return await commit(copy, "Nothing")

    # TR-5.
    assert asyncio.run(run()) is None


def test_commit_with_changes_only_inside_a_submodule_hands_back_none(
    remote: Path, tmp_path: Path
) -> None:
    library = tmp_path / "library"
    library.mkdir()
    run_git("init", "--quiet", cwd=library)
    commit_file(library, "tiles.py", "TILES = []\n")

    async def run() -> CommitId | None:
        async with started(remote, tmp_path / "work") as copy:
            add = ("-c", "protocol.file.allow=always", "submodule", "add", "--quiet")
            await git(*add, str(library), "lib", cwd=copy.path)
            await commit(copy, "Add the library")
            (copy.path / "lib" / "tiles.py").write_text("TILES = [1]\n")
            return await commit(copy, "Change the library")

    # Bug: a change only inside a submodule made the commit fail with nothing to
    # commit.
    assert asyncio.run(run()) is None


def test_push_puts_the_run_branch_on_the_remote(remote: Path, tmp_path: Path) -> None:
    async def run() -> CommitId | None:
        async with started(remote, tmp_path / "work") as copy:
            (copy.path / "TILES.md").write_text("Tiles\n")
            committed = await commit(copy, "Add the tiles")
            await push(copy)
            return committed

    committed = asyncio.run(run())

    # FR-15.
    assert tip(remote, RUN_BRANCH) == committed
