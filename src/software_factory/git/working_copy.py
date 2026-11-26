import asyncio
import os
import shutil
import stat
import tempfile
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import UTC
from pathlib import Path
from typing import TYPE_CHECKING

from software_factory.git.command import CommitId, git

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Callable
    from datetime import datetime


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
        shutil.rmtree(path, onexc=remove_read_only)


def remove_read_only(
    remove_function: Callable[[str], object], name: str, error: BaseException
) -> None:
    """Retries a removal that failed in a folder the run made read-only.

    A project's tests can leave such a folder. Without this, the error would replace
    the run's own result, even after its PR opened.
    """
    parent = Path(name).parent
    if not isinstance(error, PermissionError) or os.access(parent, os.W_OK):
        raise error
    parent.chmod(parent.stat().st_mode | stat.S_IWUSR | stat.S_IXUSR)
    remove_function(name)


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


async def start_has_file(working_copy: WorkingCopy, name: str) -> bool:
    """Whether there's a file at `name` where the run branch started."""
    entry = await git("ls-tree", working_copy.start, "--", name, cwd=working_copy.path)
    # Each line is the mode, the type, the object and the path. A folder is a tree.
    return entry.split(maxsplit=2)[1:2] == ["blob"]


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
    """Pushes the run branch to the remote from a repo of the push's own.

    A role can write the working copy's git config, such as a remote.origin.pushurl,
    or a remote.origin.receivepack that runs a command of the role's. A push from the
    working copy would then send the token where the role chose. The push's repo
    reads the working copy's commits through git's alternates file, and none of its
    config (AD-7).
    """
    branch = f"refs/heads/{working_copy.run_branch}"
    tip = await git(
        "rev-parse", "--verify", f"{branch}^{{commit}}", cwd=working_copy.path
    )
    git_dir = await git("rev-parse", "--absolute-git-dir", cwd=working_copy.path)
    with tempfile.TemporaryDirectory(prefix="push-") as folder:
        repo = Path(folder)
        await git("init", "--quiet", "--bare", cwd=repo)
        alternates = repo / "objects" / "info" / "alternates"
        await asyncio.to_thread(alternates.write_text, f"{git_dir}/objects\n")
        await git("update-ref", branch, tip, cwd=repo)
        await git(
            *("push", "--quiet", "--", working_copy.remote.url, branch),
            cwd=repo,
            token=working_copy.remote.token,
        )
