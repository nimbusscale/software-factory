import asyncio
import tempfile
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from software_factory.git.command import CommitId, git
from software_factory.git.review_copy import ReviewDiff
from software_factory.git.working_copy import remove

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from software_factory.git.working_copy import Remote

# Where the clone keeps the PR's head. GitHub keeps every PR's head at
# refs/pull/<number>/head, also for a PR from a fork, whose branch isn't in the repo.
HEAD_REF = "refs/factory/pull-request-head"


@dataclass(frozen=True)
class PullRequestClone:
    path: Path
    # The review diff for the review command (TR-25).
    diff: ReviewDiff


@asynccontextmanager
async def pull_request_clone(
    remote: Remote, number: int, base_branch: str
) -> AsyncIterator[PullRequestClone]:
    """Clones the remote with PR `number`'s head, and removes it at the end."""
    folder = Path(await asyncio.to_thread(tempfile.mkdtemp, prefix="pull-request-"))
    path = folder / "repo"
    try:
        # No checkout, since the review copy is written from the commits alone.
        await git(
            *("clone", "--quiet", "--no-checkout", "--", remote.url, str(path)),
            cwd=folder,
            token=remote.token,
        )
        await git(
            *(
                "fetch",
                "--quiet",
                "--",
                remote.url,
                f"+refs/pull/{number}/head:{HEAD_REF}",
            ),
            cwd=path,
            token=remote.token,
        )
        end = await commit_of(HEAD_REF, path)
        base = await commit_of(f"refs/remotes/origin/{base_branch}", path)
        # Meets TR-25. Where the head branched off, so changes made on the base branch
        # since then aren't in the review diff.
        start = CommitId(await git("merge-base", base, end, cwd=path))
        yield PullRequestClone(path=path, diff=ReviewDiff(start=start, end=end))
    finally:
        await asyncio.to_thread(remove, folder)


async def commit_of(ref: str, path: Path) -> CommitId:
    return CommitId(await git("rev-parse", "--verify", f"{ref}^{{commit}}", cwd=path))
