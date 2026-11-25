import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC
from typing import TYPE_CHECKING

from software_factory.git.command import CommitId, git

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Sequence
    from datetime import datetime
    from pathlib import Path


@dataclass(frozen=True)
class Clone:
    """The one clone of a repo, such as a project's, that every run on it works from."""

    path: Path


@dataclass(frozen=True)
class WorkingCopy:
    path: Path
    run_branch: str
    # The commit on the project's default branch that the run branch started from.
    start: CommitId


def run_branch_name(issue_number: int, started_at: datetime) -> str:
    """Meets TR-16, since each run starts at a time of its own."""
    # A time, not a count of earlier runs, so naming a branch needs no lookup of the
    # branches already there.
    return f"factory/issue-{issue_number}-{started_at.astimezone(UTC):%Y%m%d-%H%M%S}"


async def open_clone(remote_url: str, path: Path) -> Clone:
    """Makes the clone on the project's first run, and fetches into it on later runs."""
    if not await asyncio.to_thread(path.exists):
        await asyncio.to_thread(path.parent.mkdir, parents=True, exist_ok=True)
        await git("clone", "--quiet", "--", remote_url, str(path), cwd=path.parent)
        return Clone(path)
    await git("fetch", "--quiet", "--prune", "origin", cwd=path)
    # A fetch leaves origin/HEAD where the clone first set it. Without this, run
    # branches would go on starting from the old default branch after the project
    # changes it.
    await git("remote", "set-head", "origin", "--auto", cwd=path)
    return Clone(path)


async def default_branch_file(clone: Clone, name: str) -> str | None:
    """The file at `name` on the project's default branch, or None when there's none.

    A run branch starts from there, so it's the file the run's work starts with.
    """
    if not await git(
        "ls-tree", "--name-only", "origin/HEAD", "--", name, cwd=clone.path
    ):
        return None
    return await git("show", f"origin/HEAD:{name}", cwd=clone.path)


@asynccontextmanager
async def working_copy(
    clone: Clone, issue_number: int, started_at: datetime, path: Path
) -> AsyncIterator[WorkingCopy]:
    """Adds a worktree at `path`, on a new run branch, and removes it at the end."""
    run_branch = run_branch_name(issue_number, started_at)
    start = CommitId(await git("rev-parse", "origin/HEAD^{commit}", cwd=clone.path))
    await git(
        *("worktree", "add", "--quiet", "-b", run_branch, str(path), start),
        cwd=clone.path,
    )
    try:
        yield WorkingCopy(path=path, run_branch=run_branch, start=start)
    finally:
        # Meets TR-8. The run branch stays in the clone, so the owner can look at the
        # work of a run that ended without a PR. A run that ends early can leave
        # changes not yet committed, and git won't remove those without --force.
        await git("worktree", "remove", "--force", str(path), cwd=clone.path)


async def commit(
    working_copy: WorkingCopy, message: str, left_out: Sequence[str] = ()
) -> CommitId | None:
    """Commits every change in the working copy but those in `left_out`.

    Hands back None when there's none.
    """
    await git("add", "--all", cwd=working_copy.path)
    if left_out:
        # Unstages them whether add staged them or a role did. An exclude file can't
        # keep them out, since it doesn't apply to a file the project's repo tracks.
        await git("reset", "--quiet", "--", *left_out, cwd=working_copy.path)
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
        "push", "--quiet", "origin", working_copy.run_branch, cwd=working_copy.path
    )
