from dataclasses import dataclass
from typing import TYPE_CHECKING

from software_factory.config import factory_config
from software_factory.git.command import GitError
from software_factory.git.working_copy import (
    Remote,
    WorkingCopy,
    push,
    run_branch_name,
    start_file,
    working_copy,
)
from software_factory.github.api import GitHubError
from software_factory.github.board import Moment, end_without_pr, move_issue
from software_factory.github.issue import Issue, read_issue
from software_factory.github.pull_request import (
    OpenedPullRequestError,
    PullRequest,
    open_pull_request,
)
from software_factory.loop.rounds import (
    NothingToReviewError,
    RunContext,
    work_and_rounds,
)
from software_factory.loop.settings import SETTINGS_FILE, SettingsError, run_settings
from software_factory.roles.run import RoleFailedError, RoleRunner

if TYPE_CHECKING:
    from collections.abc import Callable
    from datetime import datetime
    from pathlib import Path

    from software_factory.github.api import GraphQL, Repo

# The errors that end a run with a reason for the owner (TR-2, FR-7, TR-15, TR-18).
RUN_ENDING_ERRORS = (RoleFailedError, GitError, GitHubError, NothingToReviewError)


class RunRefusedError(Exception):
    """The run didn't start, so the issue and its board are as they were (FR-5, FR-26).

    The message says why, in words for the owner.
    """


class RunEndedError(Exception):
    """The run ended without a PR, and the issue says why (FR-13, FR-14)."""


@dataclass(frozen=True)
class RunRequest:
    repo: Repo
    issue_number: int
    # The number of rounds the command sets, or None when it sets none.
    rounds: int | None
    started_at: datetime


@dataclass(frozen=True)
class Services:
    graphql: GraphQL
    runner: RoleRunner
    # The folder that holds each run's working copy.
    home: Path
    remote: Callable[[Repo], Remote]
    factory_version: str


def github_remote(repo: Repo, token: str) -> Remote:
    return Remote(url=f"https://github.com/{repo}.git", token=token)


async def run(request: RunRequest, services: Services) -> PullRequest:
    """Meets FR-1. Hands back the run's PR.

    Raises RunRefusedError when the run doesn't start, RunEndedError when it ends
    without a PR, and OpenedPullRequestError when it ends after opening one.
    """
    repo = request.repo
    branch = run_branch_name(request.issue_number, request.started_at)
    path = (services.home / "working-copies" / repo.owner / repo.name) / branch.replace(
        "/", "-"
    )
    remote = services.remote(repo)
    try:
        async with working_copy(
            remote, request.issue_number, request.started_at, path
        ) as copy:
            return await run_in(request, services, copy)
    except GitError as error:
        # Only the clone and the read of the settings file raise it here, since the
        # run ends on any git error after them.
        raise RunRefusedError(str(error)) from error


async def run_in(
    request: RunRequest, services: Services, copy: WorkingCopy
) -> PullRequest:
    """Runs in the working copy. Refuses the run before anything changes on GitHub."""
    try:
        settings = run_settings(await read_settings_file(copy), request.rounds)
        issue = await read_issue(services.graphql, request.repo, request.issue_number)
    except (SettingsError, GitHubError) as error:
        raise RunRefusedError(str(error)) from error
    try:
        await move_issue(services.graphql, request.repo, issue, Moment.RUN_STARTED)
        record = await work_and_rounds(
            RunContext(issue, copy, settings, services.runner)
        )
        await push(copy)
        # Meets FR-15.
        return await open_pull_request(
            services.graphql, request.repo, record, services.factory_version
        )
    except OpenedPullRequestError:
        raise
    except RUN_ENDING_ERRORS as error:
        reason = await with_work_on_github(copy, str(error))
        raise await end_run(request, services, issue, reason) from error
    except Exception as error:
        reason = f"The workflow failed with an error it doesn't handle: {error!r}"
        await end_run(request, services, issue, await with_work_on_github(copy, reason))
        raise


async def read_settings_file(copy: WorkingCopy) -> str | None:
    try:
        return await start_file(copy, SETTINGS_FILE)
    except UnicodeDecodeError as error:
        message = f"The project's {SETTINGS_FILE} isn't UTF-8 text: {error}"
        raise SettingsError(message) from error


async def with_work_on_github(copy: WorkingCopy, reason: str) -> str:
    """Pushes the run branch of a run that ends without a PR (FR-34).

    Hands back `reason`, with where the work is or why it isn't on GitHub.
    """
    try:
        await push(copy)
    except GitError as error:
        return f"{reason}\n\nThe run branch couldn't be put on GitHub: {error}"
    return f"{reason}\n\nThe run's work is on the branch `{copy.run_branch}`."


async def end_run(
    request: RunRequest, services: Services, issue: Issue, reason: str
) -> RunEndedError:
    """Moves the issue to Needs attention and posts why, and hands back the error."""
    try:
        await end_without_pr(services.graphql, request.repo, issue, reason)
    except GitHubError as error:
        status = factory_config().statuses["needs_attention"].name
        return RunEndedError(
            f"{reason}\n\nThe issue couldn't be moved to {status}: {error}"
        )
    return RunEndedError(reason)
