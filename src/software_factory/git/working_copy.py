import asyncio
import shutil
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC
from typing import TYPE_CHECKING

from software_factory.git.command import CommitId, git

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from datetime import datetime
    from pathlib import Path


@dataclass(frozen=True)
class Remote:
    """The project's repo on GitHub, which each run clones."""

    url: str
    # The token git sends when the remote asks for one, or None when it asks for
    # none. Out of the repr, so an error that prints the remote doesn't print it.
    token: str | None = field(default=None, repr=False)


@dataclass(frozen=True)
class WorkingCopy:
    path: Path
    remote: Remote
    run_branch: str
    # The commit on the project's default branch that the run branch started from.
    start: CommitId


def run_branch_name(issue_number: int, started_at: datetime) -> str:
    """Meets TR-16, since each run starts at a time of its own."""
    # A time, not a count of earlier runs, so naming a branch needs no lookup of the
    # branches already there.
    return f"factory/issue-{issue_number}-{started_at.astimezone(UTC):%Y%m%d-%H%M%S}"


@asynccontextmanager
async def working_copy(
    remote: Remote, issue_number: int, started_at: datetime, path: Path
) -> AsyncIterator[WorkingCopy]:
    """Clones the remote at `path`, on a new run branch, and removes it at the end.

    Each run clones the remote afresh, and keeps nothing from an earlier run.
    """
    run_branch = run_branch_name(issue_number, started_at)
    try:
        await asyncio.to_thread(path.parent.mkdir, parents=True, exist_ok=True)
        await git(
            *("clone", "--quiet", "--", remote.url, str(path)),
            cwd=path.parent,
            token=remote.token,
        )
        start = CommitId(await git("rev-parse", "HEAD^{commit}", cwd=path))
        await git("switch", "--quiet", "--create", run_branch, cwd=path)
        yield WorkingCopy(path=path, remote=remote, run_branch=run_branch, start=start)
    finally:
        # Meets TR-8.
        await asyncio.to_thread(remove, path)


def remove(path: Path) -> None:
    # A clone that failed can leave no folder.
    if path.exists():
        shutil.rmtree(path)


async def start_file(working_copy: WorkingCopy, name: str) -> str | None:
    """The file at `name` where the run branch started, or None when there's none.

    That's the file on the project's default branch, which the run's work starts with.
    """
    start = working_copy.start
    if not await git(
        "ls-tree", "--name-only", start, "--", name, cwd=working_copy.path
    ):
        return None
    return await git("show", f"{start}:{name}", cwd=working_copy.path)


async def commit(working_copy: WorkingCopy, message: str) -> CommitId | None:
    """Commits every change in the working copy. Hands back None when there's none."""
    await git("add", "--all", cwd=working_copy.path)
    # Not git status, which also lists changes inside a submodule that add doesn't
    # stage, so commit would then fail with nothing to commit.
    if not await git("diff", "--cached", "--name-only", cwd=working_copy.path):
        return None
    await git("commit", "--quiet", "--message", message, cwd=working_copy.path)
    return await head(working_copy)


async def head(working_copy: WorkingCopy) -> CommitId:
    return CommitId(await git("rev-parse", "HEAD", cwd=working_copy.path))


async def push(working_copy: WorkingCopy) -> None:
    await git(
        *("push", "--quiet", "origin", working_copy.run_branch),
        cwd=working_copy.path,
        token=working_copy.remote.token,
    )
