import asyncio
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from software_factory.git.command import git
from software_factory.git.review_copy import ReviewDiff, review_copy, review_diff
from software_factory.git.working_copy import (
    WorkingCopy,
    commit,
    open_clone,
    working_copy,
)

STARTED = datetime(2026, 11, 24, 21, 30, 0, tzinfo=UTC)

if TYPE_CHECKING:
    from pathlib import Path

    from software_factory.git.command import CommitId


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
        clone = await open_clone(str(remote), tmp_path / "clone")
        async with working_copy(clone, 7, STARTED, tmp_path / "work") as copy:
            work_commit = await committed(copy, {"TILES.md": "Tiles\n"})
            first = await review_diff(copy, None)
            answer_commit = await committed(copy, {"TILES.md": "Fixed tiles\n"})
            second = await review_diff(copy, first)

            assert first == ReviewDiff(start=copy.start, end=work_commit)
            assert second == ReviewDiff(start=work_commit, end=answer_commit)

    asyncio.run(run())


def test_review_copy_holds_the_review_diff_as_changes_not_yet_committed(
    remote: Path, tmp_path: Path
) -> None:
    async def run() -> None:
        clone = await open_clone(str(remote), tmp_path / "clone")
        async with working_copy(clone, 7, STARTED, tmp_path / "work") as copy:
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
        clone = await open_clone(str(remote), tmp_path / "clone")
        async with working_copy(clone, 7, STARTED, tmp_path / "work") as copy:
            files: dict[str, str | None] = {
                ".gitattributes": "TILES.md export-ignore\n",
                "TILES.md": "Tiles\n",
            }
            await committed(copy, files)
            diff = await review_diff(copy, None)
            async with review_copy(copy, diff) as path:
                assert (path / "TILES.md").read_text() == "Tiles\n"

    asyncio.run(run())
