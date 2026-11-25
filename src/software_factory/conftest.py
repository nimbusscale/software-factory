import asyncio
from typing import TYPE_CHECKING

import pytest

from software_factory.git.command import CommitId, git

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

# A small copy of the factory's doc standards, on its repo's main branch.
FACTORY_STANDARDS = {
    "docs/standards/README.md": "The factory's doc standards.\n",
    "docs/standards/review-rubric.md": "The factory's review rubric.\n",
    "tools/check-docs.sh": "echo The factory's doc check\n",
}


@pytest.fixture(autouse=True)
def git_config(
    tmp_path_factory: pytest.TempPathFactory, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Gives git an identity of its own, and keeps the machine's git config out."""
    # Not in tmp_path, which some tests list.
    config = tmp_path_factory.mktemp("git") / "gitconfig"
    config.write_text(
        "[user]\n\tname = Test\n\temail = test@localhost\n"
        "[init]\n\tdefaultBranch = main\n"
    )
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def run_git(*args: str, cwd: Path) -> str:
    return asyncio.run(git(*args, cwd=cwd))


def commit_file(repo: Path, name: str, text: str) -> CommitId:
    (repo / name).write_text(text)
    run_git("add", "--all", cwd=repo)
    run_git("commit", "--quiet", "--message", f"Add {name}", cwd=repo)
    return CommitId(run_git("rev-parse", "HEAD", cwd=repo))


def commit_files(repo: Path, files: Mapping[str, str], message: str) -> CommitId:
    for name, text in files.items():
        (repo / name).parent.mkdir(parents=True, exist_ok=True)
        (repo / name).write_text(text)
    run_git("add", "--all", cwd=repo)
    run_git("commit", "--quiet", "--message", message, cwd=repo)
    return CommitId(run_git("rev-parse", "HEAD", cwd=repo))


def make_factory_remote(folder: Path) -> Path:
    """A bare repo in `folder` that plays the factory's, unless one is there already.

    Its author is at factory-author in `folder`, for a test to push more to it.
    """
    bare = folder / "factory.git"
    if bare.exists():
        return bare
    seed = folder / "factory-seed"
    seed.mkdir()
    run_git("init", "--quiet", cwd=seed)
    commit_files(seed, FACTORY_STANDARDS, "Add the doc standards")
    run_git("clone", "--quiet", "--bare", str(seed), str(bare), cwd=folder)
    run_git("clone", "--quiet", str(bare), "factory-author", cwd=folder)
    return bare


@pytest.fixture
def factory_remote(tmp_path: Path) -> Path:
    return make_factory_remote(tmp_path)


@pytest.fixture
def author(tmp_path: Path) -> Path:
    """A clone of the remote, where a test plays someone pushing to the project."""
    seed = tmp_path / "seed"
    seed.mkdir()
    run_git("init", "--quiet", cwd=seed)
    commit_file(seed, "README.md", "Dust Law\n")
    run_git("clone", "--quiet", "--bare", str(seed), "remote.git", cwd=tmp_path)
    run_git("clone", "--quiet", "remote.git", "author", cwd=tmp_path)
    return tmp_path / "author"


@pytest.fixture
def remote(author: Path) -> Path:
    return author.parent / "remote.git"
