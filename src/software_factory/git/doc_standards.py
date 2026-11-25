import asyncio
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from software_factory.git.command import CommitId, GitError, git, write_files

if TYPE_CHECKING:
    from software_factory.git.working_copy import Clone, WorkingCopy

# Meets TD-13.
DOC_STANDARDS_PATHS = ("docs/standards", "tools/check-docs.sh")


class DocStandardsError(Exception):
    """The branch FR-33 picks doesn't give the doc standards (FR-34).

    The message says why, in words for the owner.
    """


@dataclass(frozen=True)
class DocStandards:
    # The clone of the factory's own repo.
    clone: Clone
    # The commit they come from (FR-37).
    commit: CommitId


async def find_doc_standards(clone: Clone, branch: str) -> DocStandards:
    """The doc standards at the tip of `branch` in the factory's repo."""
    # The branch on GitHub, as the latest fetch left it. The clone's own branch of
    # the same name stays where the clone first made it.
    ref = f"refs/remotes/origin/{branch}^{{commit}}"
    try:
        commit = CommitId(
            await git("rev-parse", "--verify", "--quiet", ref, cwd=clone.path)
        )
    except GitError as error:
        message = f"The factory's repo has no branch {branch}."
        raise DocStandardsError(message) from error
    for name in DOC_STANDARDS_PATHS:
        if not await git("ls-tree", "--name-only", commit, "--", name, cwd=clone.path):
            message = f"The factory's branch {branch} has no {name}."
            raise DocStandardsError(message)
    return DocStandards(clone=clone, commit=commit)


async def write_doc_standards(standards: DocStandards, path: Path) -> None:
    """Puts the doc standards in the folder at `path`, in place of what's there."""
    await asyncio.to_thread(remove_doc_standards, path)
    await write_files(standards.clone.path, standards.commit, path, DOC_STANDARDS_PATHS)


def remove_doc_standards(path: Path) -> None:
    """Deletes what's at the doc standards' paths in `path`, such as a project copy."""
    for name in DOC_STANDARDS_PATHS:
        target = path / name
        if target.is_dir() and not target.is_symlink():
            shutil.rmtree(target)
        elif target.exists() or target.is_symlink():
            target.unlink()


async def exclude_doc_standards(working_copy: WorkingCopy) -> None:
    """Lists the doc standards in the clone's exclude file, unless they're there."""
    # Then git status doesn't show the implementer the doc standards as its own new
    # files, and the doc check script doesn't read the script as one of the project's
    # source files. The clone's exclude file, since a worktree has none of its own.
    exclude = Path(
        await git(
            *("rev-parse", "--path-format=absolute", "--git-path", "info/exclude"),
            cwd=working_copy.path,
        )
    )
    await asyncio.to_thread(
        add_lines, exclude, [f"/{name}" for name in DOC_STANDARDS_PATHS]
    )


def add_lines(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    missing = [line for line in lines if line not in text.splitlines()]
    if not missing:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + "".join(f"{line}\n" for line in missing), encoding="utf-8")
