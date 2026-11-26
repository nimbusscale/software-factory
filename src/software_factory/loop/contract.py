"""The checks of the project contract, and the project's make targets."""

import asyncio
import contextlib
import os
import shutil
import signal
import tempfile
from typing import IO, TYPE_CHECKING

from software_factory.git.command import GITHUB_TOKEN_VARIABLES, REPO_ENV_VARS
from software_factory.git.working_copy import changed_files, start_has_file

if TYPE_CHECKING:
    from pathlib import Path

    from software_factory.git.working_copy import WorkingCopy

SPECS = {
    "functional spec": "docs/functional-spec.md",
    "technical spec": "docs/technical-spec.md",
}

# Every run waits for both targets before any work starts, so a slow setup or check
# slows every issue. A project whose targets need longer needs a faster setup or
# check, not a longer limit.
TIME_LIMIT_SECONDS = 10 * 60

# The targets run the project's own commands, so they get no token. These are the
# variables Claude Code reads its token from (AD-7 for the GitHub token).
CLAUDE_TOKEN_VARIABLES = frozenset(
    {"CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"}
)
LEFT_OUT = CLAUDE_TOKEN_VARIABLES | GITHUB_TOKEN_VARIABLES | REPO_ENV_VARS

# How much of the end of a target's output a reason holds.
OUTPUT_LINES = 30
OUTPUT_BYTES = 64 * 1024
# The most files a reason names.
LISTED_FILES = 10


class ContractError(Exception):
    """The project doesn't meet the project contract. The message says why."""


async def check_contract(working_copy: WorkingCopy) -> None:
    """Meets FR-35, FR-36, FR-37 and FR-38, before the run makes any change."""
    missing = [
        f"The project has no {name} at `{path}`."
        for name, path in SPECS.items()
        if not await start_has_file(working_copy, path)
    ]
    if missing:
        raise ContractError(" ".join(missing))
    for target in ("setup", "check"):
        await make(target, working_copy.path, "the working copy")
        # Checked after each target, so the reason names the one that left them.
        await left_no_files(target, working_copy)


async def left_no_files(target: str, working_copy: WorkingCopy) -> None:
    files = await changed_files(working_copy)
    if not files:
        return
    listed = ", ".join(f"`{name}`" for name in files[:LISTED_FILES])
    more = len(files) - LISTED_FILES
    if more > 0:
        listed += f" and {more} more"
    message = (
        f"`make {target}` added or changed files that git doesn't ignore: {listed}."
        " The run would commit them with its work."
    )
    raise ContractError(message)


async def make(
    target: str, cwd: Path, place: str, time_limit: float = TIME_LIMIT_SECONDS
) -> None:
    """Runs `make <target>` in `cwd`, which `place` names for the owner.

    Raises ContractError when it fails, or runs past `time_limit`, in seconds.
    """
    executable = shutil.which("make")
    if executable is None:
        message = "make isn't installed, or isn't on the PATH."
        raise ContractError(message)
    env = {name: value for name, value in os.environ.items() if name not in LEFT_OUT}
    # A file, not a pipe, so a process the target leaves running can't keep the
    # read from ending.
    with tempfile.TemporaryFile() as output:
        process = await asyncio.create_subprocess_exec(
            *(executable, target),
            cwd=cwd,
            env=env,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=output,
            stderr=asyncio.subprocess.STDOUT,
            # So a stop at the time limit stops every process the target started.
            start_new_session=True,
        )
        try:
            async with asyncio.timeout(time_limit):
                code = await process.wait()
        except TimeoutError:
            message = (
                f"`make {target}` in {place} ran past its time limit of"
                f" {time_limit / 60:g} minutes."
            )
            raise ContractError(message + end_of(output)) from None
        finally:
            if process.returncode is None:
                stop(process.pid)
                await process.wait()
        if code != 0:
            message = f"`make {target}` failed in {place}, with exit code {code}."
            raise ContractError(message + end_of(output))


def stop(process_group: int) -> None:
    # The group can be gone already, when its last process ended on its own.
    with contextlib.suppress(ProcessLookupError):
        os.killpg(process_group, signal.SIGKILL)


def end_of(output: IO[bytes]) -> str:
    """The end of a target's output, as a code block that follows a reason."""
    size = output.seek(0, os.SEEK_END)
    output.seek(max(0, size - OUTPUT_BYTES))
    lines = output.read().decode(errors="replace").splitlines()[-OUTPUT_LINES:]
    if not lines:
        return " It printed nothing."
    text = "\n".join(lines)
    # A fence longer than any run of backticks in the output, so none of it ends
    # the block.
    fence = "`" * max(3, longest_run(text, "`") + 1)
    return f" The end of its output:\n\n{fence}\n{text}\n{fence}"


def longest_run(text: str, character: str) -> int:
    longest = run = 0
    for each in text:
        run = run + 1 if each == character else 0
        longest = max(longest, run)
    return longest
