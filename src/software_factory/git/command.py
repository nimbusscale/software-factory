import asyncio
import os
import shutil
from typing import TYPE_CHECKING, NewType

if TYPE_CHECKING:
    from collections.abc import Mapping
    from pathlib import Path

CommitId = NewType("CommitId", str)

# What `git rev-parse --local-env-vars` lists in git 2.34: the variables, such as
# GIT_DIR, that point git at a repo other than the one in `cwd`. Git sets some of them
# for its hooks. So without dropping them, git run from a hook, such as the tests the
# pre-commit hook runs, works in the hook's repo.
REPO_ENV_VARS = frozenset(
    {
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
        "GIT_CONFIG",
        "GIT_CONFIG_PARAMETERS",
        "GIT_CONFIG_COUNT",
        "GIT_OBJECT_DIRECTORY",
        "GIT_DIR",
        "GIT_WORK_TREE",
        "GIT_IMPLICIT_WORK_TREE",
        "GIT_GRAFT_FILE",
        "GIT_INDEX_FILE",
        "GIT_NO_REPLACE_OBJECTS",
        "GIT_REPLACE_REF_BASE",
        "GIT_PREFIX",
        "GIT_INTERNAL_SUPER_PREFIX",
        "GIT_SHALLOW_FILE",
        "GIT_COMMON_DIR",
    }
)


# Over HTTPS, git waits with no limit for a server that accepted the connection and
# then went silent. With these, it gives up once a transfer stays under 1000 bytes a
# second for 60 seconds. A slow clone that's still moving never trips them.
STALL_CHECK = (*("-c", "http.lowSpeedLimit=1000", "-c", "http.lowSpeedTime=60"),)


class GitError(Exception):
    pass


async def git(*args: str, cwd: Path, extra_env: Mapping[str, str] | None = None) -> str:
    """Hands back what git printed, without its trailing newline."""
    env = {
        name: value for name, value in os.environ.items() if name not in REPO_ENV_VARS
    }
    # A run has no one at the terminal, so git fails rather than wait for a username.
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.update(extra_env or {})
    executable = shutil.which("git")
    if executable is None:
        message = "git isn't installed, or isn't on the PATH."
        raise GitError(message)
    process = await asyncio.create_subprocess_exec(
        executable,
        *STALL_CHECK,
        *args,
        cwd=cwd,
        env=env,
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        # Git prints its errors in the machine's locale, which may not be UTF-8.
        error = stderr.decode(errors="replace").strip()
        message = f"git {' '.join(args)} failed: {error}"
        raise GitError(message)
    return stdout.decode().rstrip("\n")
