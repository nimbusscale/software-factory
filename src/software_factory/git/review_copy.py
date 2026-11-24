import asyncio
import os
import shutil
import tempfile
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from software_factory.git.command import CommitId, git
from software_factory.git.working_copy import WorkingCopy, head

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

# The base commit is only there so the review diff shows as changes not yet committed.
# So it has a fixed author, and turns off signing and every hook, which have nothing to
# check here. It then works on a machine with no git identity or signing key, and the
# machine's git identity stays out of the review copy (TR-7). The author is set through
# these variables, since they win over git config, and git sets them for its hooks.
BASE_COMMIT_AUTHOR = {
    "GIT_AUTHOR_NAME": "Software factory",
    "GIT_AUTHOR_EMAIL": "factory@localhost",
    "GIT_COMMITTER_NAME": "Software factory",
    "GIT_COMMITTER_EMAIL": "factory@localhost",
}
BASE_COMMIT = (
    *("-c", "commit.gpgsign=false", "-c", f"core.hooksPath={os.devnull}"),
    *("commit", "--quiet", "--allow-empty", "--message", "base"),
)

# --force, since a project can track a file that its .gitignore matches, and a plain
# add leaves such a file out. Every file in the review copy is one the project tracks.
ADD_EVERY_FILE = ("add", "--all", "--force")


@dataclass(frozen=True)
class ReviewDiff:
    start: CommitId
    end: CommitId


async def review_diff(
    working_copy: WorkingCopy, previous: ReviewDiff | None
) -> ReviewDiff:
    """The round's review diff (TR-3, TR-4).

    `previous` is the previous round's review diff, or None in the first round.
    """
    start = working_copy.start if previous is None else previous.end
    return ReviewDiff(start=start, end=await head(working_copy))


@asynccontextmanager
async def review_copy(
    working_copy: WorkingCopy, diff: ReviewDiff
) -> AsyncIterator[Path]:
    """A new folder that holds the review copy (TD-2), removed when the block ends."""
    path = Path(await asyncio.to_thread(tempfile.mkdtemp, prefix="review-copy-"))
    try:
        await git("init", "--quiet", cwd=path)
        await write_files(working_copy, diff.start, path)
        await git(*ADD_EVERY_FILE, cwd=path)
        await git(*BASE_COMMIT, cwd=path, extra_env=BASE_COMMIT_AUTHOR)
        await asyncio.to_thread(clear, path)
        await write_files(working_copy, diff.end, path)
        # Staged, so `git diff HEAD` shows the files the review diff adds. Left
        # unstaged, they'd be untracked, and missing from it.
        await git(*ADD_EVERY_FILE, cwd=path)
        yield path
    finally:
        await asyncio.to_thread(shutil.rmtree, path)


async def write_files(working_copy: WorkingCopy, commit: CommitId, path: Path) -> None:
    """Writes the files as they stood at `commit` into `path`, with no git history."""
    # Not git archive, which leaves out the files a project marks export-ignore. A
    # separate index, so the working copy's own index stays as it is.
    with tempfile.TemporaryDirectory() as index_folder:
        index = {"GIT_INDEX_FILE": str(Path(index_folder) / "index")}
        await git("read-tree", commit, cwd=working_copy.path, extra_env=index)
        await git(
            *("checkout-index", "--all", f"--prefix={path}{os.sep}"),
            cwd=working_copy.path,
            extra_env=index,
        )


def clear(path: Path) -> None:
    """Deletes everything in `path` but the review copy's own git folder."""
    for child in path.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
