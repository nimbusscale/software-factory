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

# The GitHub token reaches git only in this variable, set for the one command that
# needs it, so it's never in git's config or any other file a role can read (AD-7).
LOGIN_VARIABLE = "SOFTWARE_FACTORY_GIT_TOKEN"
# The empty helper first clears any helper git's config names, so git asks only this
# one. A helper is called with get, store or erase, and only get is answered. Hooks
# are off, since the token is in the environment of every hook git starts.
WITH_TOKEN = (
    *("-c", "credential.helper=", "-c", f"core.hooksPath={os.devnull}"),
    "-c",
    (
        'credential.helper=!f() { test "$1" = get'
        " && echo username=x-access-token"
        f' && echo "password=${LOGIN_VARIABLE}"; }}; f'
    ),
)
# The variables the GitHub CLI reads its token from. They're left out of every git
# command, so a hook that git starts never gets them.
GITHUB_TOKEN_VARIABLES = frozenset({"GH_TOKEN", "GITHUB_TOKEN"})


class GitError(Exception):
    pass


async def git(
    *args: str,
    cwd: Path,
    extra_env: Mapping[str, str] | None = None,
    token: str | None = None,
) -> str:
    """Hands back what git printed, without its trailing newline.

    `token` is the token git sends when the remote asks for one.
    """
    left_out = REPO_ENV_VARS | GITHUB_TOKEN_VARIABLES
    env = {name: value for name, value in os.environ.items() if name not in left_out}
    # A run has no one at the terminal, so git fails rather than wait for a username.
    env["GIT_TERMINAL_PROMPT"] = "0"
    env.update(extra_env or {})
    auth: tuple[str, ...] = ()
    if token is not None:
        auth = WITH_TOKEN
        env[LOGIN_VARIABLE] = token
    executable = shutil.which("git")
    if executable is None:
        message = "git isn't installed, or isn't on the PATH."
        raise GitError(message)
    process = await asyncio.create_subprocess_exec(
        executable,
        *STALL_CHECK,
        *auth,
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
