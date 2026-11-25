import asyncio
from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest

from software_factory.conftest import FACTORY_STANDARDS, commit_files, run_git
from software_factory.git.command import git
from software_factory.git.doc_standards import (
    DOC_STANDARDS_PATHS,
    DocStandardsError,
    exclude_doc_standards,
    find_doc_standards,
    write_doc_standards,
)
from software_factory.git.working_copy import commit, open_clone, working_copy

if TYPE_CHECKING:
    from pathlib import Path

STARTED = datetime(2026, 11, 24, 21, 30, 0, tzinfo=UTC)


def push_branch(factory_remote: Path, branch: str, files: dict[str, str]) -> None:
    """Pushes a new branch of the factory's repo with `files` changed."""
    author = factory_remote.parent / "factory-author"
    run_git("switch", "--quiet", "-c", branch, cwd=author)
    commit_files(author, files, f"Change {', '.join(files)}")
    run_git("push", "--quiet", "origin", branch, cwd=author)
    run_git("switch", "--quiet", "main", cwd=author)


def test_finds_the_standards_at_the_tip_of_the_branch(
    factory_remote: Path, tmp_path: Path
) -> None:
    push_branch(factory_remote, "trial", {"docs/standards/README.md": "Trial.\n"})
    tip = run_git("rev-parse", "trial", cwd=factory_remote)

    async def run() -> None:
        clone = await open_clone(str(factory_remote), tmp_path / "clone")
        standards = await find_doc_standards(clone, "trial")
        assert standards.commit == tip

    asyncio.run(run())


@pytest.mark.parametrize(
    "case",
    [
        ("missing", "The factory's repo has no branch missing."),
        ("no-script", "The factory's branch no-script has no tools/check-docs.sh."),
    ],
)
def test_branch_without_the_standards_is_refused(
    factory_remote: Path, tmp_path: Path, case: tuple[str, str]
) -> None:
    """Meets FR-34."""
    author = factory_remote.parent / "factory-author"
    run_git("switch", "--quiet", "-c", "no-script", cwd=author)
    run_git("rm", "--quiet", "tools/check-docs.sh", cwd=author)
    run_git("commit", "--quiet", "--message", "Drop the script", cwd=author)
    run_git("push", "--quiet", "origin", "no-script", cwd=author)
    branch, message = case

    async def run() -> None:
        clone = await open_clone(str(factory_remote), tmp_path / "clone")
        with pytest.raises(DocStandardsError, match=message):
            await find_doc_standards(clone, branch)

    asyncio.run(run())


def test_write_replaces_the_projects_copy(factory_remote: Path, tmp_path: Path) -> None:
    folder = tmp_path / "copy"
    project_files = {
        "docs/standards/README.md": "The project's standards.\n",
        "docs/standards/extra.md": "A file only the project has.\n",
        "docs/functional-spec.md": "The project's spec.\n",
    }
    for name, text in project_files.items():
        (folder / name).parent.mkdir(parents=True, exist_ok=True)
        (folder / name).write_text(text)

    async def run() -> None:
        clone = await open_clone(str(factory_remote), tmp_path / "clone")
        await write_doc_standards(await find_doc_standards(clone, "main"), folder)

    asyncio.run(run())

    for name, text in FACTORY_STANDARDS.items():
        assert (folder / name).read_text() == text
    assert not (folder / "docs/standards/extra.md").exists()
    assert (folder / "docs/functional-spec.md").read_text() == "The project's spec.\n"


def test_excluded_standards_are_left_out_of_git_status_and_commits(
    remote: Path, factory_remote: Path, tmp_path: Path
) -> None:
    async def run() -> None:
        clone = await open_clone(str(remote), tmp_path / "clone")
        factory = await open_clone(str(factory_remote), tmp_path / "factory-clone")
        standards = await find_doc_standards(factory, "main")
        async with working_copy(clone, 7, STARTED, tmp_path / "work") as copy:
            await exclude_doc_standards(copy)
            await exclude_doc_standards(copy)
            await write_doc_standards(standards, copy.path)
            assert await git("status", "--porcelain", cwd=copy.path) == ""
            assert await commit(copy, "Nothing", DOC_STANDARDS_PATHS) is None

    asyncio.run(run())
    exclude = (tmp_path / "clone" / ".git" / "info" / "exclude").read_text()
    assert exclude.splitlines().count("/docs/standards") == 1
