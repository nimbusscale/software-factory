import asyncio
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from software_factory.git.command import git
from software_factory.git.review_copy import ReviewDiff, review_copy, review_diff
from software_factory.git.working_copy import (
    Remote,
    WorkingCopy,
    commit,
    working_copy,
)

STARTED = datetime(2026, 11, 24, 21, 30, 0, tzinfo=UTC)

if TYPE_CHECKING:
    from contextlib import AbstractAsyncContextManager
    from pathlib import Path

    from software_factory.git.command import CommitId


def started(remote: Path, tmp_path: Path) -> AbstractAsyncContextManager[WorkingCopy]:
    return working_copy(Remote(str(remote)), 7, STARTED, tmp_path / "work")


def work(path: Path, files: dict[str, str | None]) -> None:
    """Writes each file, or deletes it where its text is None."""
    for name, text in files.items():
        if text is None:
            (path / name).unlink()
        else:
            (path / name).write_text(text)


async def committed(copy: WorkingCopy, files: dict[str, str | None]) -> CommitId:
    work(copy.path, files)
    commit_id = await commit(copy, f"Change {', '.join(files)}")
    assert commit_id is not None
    return commit_id


def test_review_diffs_cover_the_work_then_each_answer(
    remote: Path, tmp_path: Path
) -> None:
    async def run() -> None:
        async with started(remote, tmp_path) as copy:
            work_commit = await committed(copy, {"TILES.md": "Tiles\n"})
            first = await review_diff(copy, None)
            answer_commit = await committed(copy, {"TILES.md": "Fixed tiles\n"})
            second = await review_diff(copy, first)

            # TR-3.
            assert first == ReviewDiff(start=copy.start, end=work_commit)
            # TR-4.
            assert second == ReviewDiff(start=work_commit, end=answer_commit)

    asyncio.run(run())


def test_review_copy_holds_the_review_diff_as_changes_not_yet_committed(
    remote: Path, tmp_path: Path
) -> None:
    async def run() -> None:
        async with started(remote, tmp_path) as copy:
            await committed(copy, {"TILES.md": "Tiles\n", "RULES.md": "Rules\n"})
            first = await review_diff(copy, None)
            await committed(
                copy,
                {"TILES.md": "Fixed tiles\n", "RULES.md": None, "LAWS.md": "Laws\n"},
            )
            second = await review_diff(copy, first)
            (copy.path / "NOTES.md").write_text("Staged\n")
            await git("add", "NOTES.md", cwd=copy.path)
            async with review_copy(copy, second) as path:
                # TD-2.
                await check_review_copy(path)
            assert not path.exists()
            assert await git("status", "--porcelain", cwd=copy.path) == "A  NOTES.md"

    asyncio.run(run())


async def check_review_copy(path: Path) -> None:
    log = await git("log", "--format=%an %s", cwd=path)
    assert log == "Software factory base"
    base_files = await git("ls-tree", "-r", "--name-only", "HEAD", cwd=path)
    assert base_files.splitlines() == ["README.md", "RULES.md", "TILES.md"]
    changes = await git("diff", "HEAD", "--name-status", cwd=path)
    assert changes.splitlines() == ["A\tLAWS.md", "D\tRULES.md", "M\tTILES.md"]
    assert (path / "TILES.md").read_text() == "Fixed tiles\n"


def test_review_copy_holds_files_marked_export_ignore(
    remote: Path, tmp_path: Path
) -> None:
    async def run() -> None:
        async with started(remote, tmp_path) as copy:
            files: dict[str, str | None] = {
                ".gitattributes": "TILES.md export-ignore\n",
                "TILES.md": "Tiles\n",
            }
            await committed(copy, files)
            diff = await review_diff(copy, None)
            async with review_copy(copy, diff) as path:
                # TD-2.
                assert (path / "TILES.md").read_text() == "Tiles\n"

    asyncio.run(run())


def test_review_copy_holds_tracked_files_the_project_ignores(
    remote: Path, tmp_path: Path
) -> None:
    async def run() -> None:
        async with started(remote, tmp_path) as copy:
            work(copy.path, {".gitignore": "*.env\n", "example.env": "A=1\n"})
            await git("add", "--force", "example.env", cwd=copy.path)
            await commit(copy, "Add an example env file")
            first = await review_diff(copy, None)
            await committed(copy, {"example.env": "A=2\n"})
            second = await review_diff(copy, first)
            async with review_copy(copy, second) as path:
                changes = await git("diff", "HEAD", "--name-status", cwd=path)
                # TD-2.
                assert changes == "M\texample.env"

    asyncio.run(run())


def test_base_commit_skips_the_machines_signing_and_hooks(
    remote: Path, tmp_path: Path
) -> None:
    hooks = tmp_path / "hooks"
    hooks.mkdir()
    for hook in ("pre-commit", "prepare-commit-msg", "post-commit"):
        (hooks / hook).write_text("#!/bin/sh\nexit 1\n")
        (hooks / hook).chmod(0o755)

    async def run() -> None:
        async with started(remote, tmp_path) as copy:
            await committed(copy, {"TILES.md": "Tiles\n"})
            diff = await review_diff(copy, None)
            for setting in ("commit.gpgsign=true", "gpg.program=false"):
                await git("config", "--global", *setting.split("="), cwd=copy.path)
            await git("config", "--global", "core.hooksPath", str(hooks), cwd=copy.path)
            async with review_copy(copy, diff) as path:
                # TD-2.
                assert await git("log", "--format=%s", cwd=path) == "base"

    asyncio.run(run())
