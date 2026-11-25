from dataclasses import dataclass
from typing import TYPE_CHECKING

from software_factory.config import factory_config
from software_factory.git.command import GitError
from software_factory.git.doc_standards import (
    DocStandardsError,
    exclude_doc_standards,
    find_doc_standards,
    write_doc_standards,
)
from software_factory.git.working_copy import (
    default_branch_file,
    open_clone,
    push,
    run_branch_name,
    working_copy,
)
from software_factory.github.api import GitHubError, Repo
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

    from software_factory.config import Settings
    from software_factory.git.doc_standards import DocStandards
    from software_factory.git.working_copy import Clone
    from software_factory.github.api import GraphQL

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
    # The branch of the factory's repo the command names, or None when it names none.
    doc_standards_branch: str | None = None


@dataclass(frozen=True)
class Services:
    graphql: GraphQL
    runner: RoleRunner
    # The folder that holds each repo's clone and each run's working copy.
    home: Path
    remote_url: Callable[[Repo], str]


@dataclass(frozen=True)
class Setup:
    clone: Clone
    settings: Settings
    doc_standards: DocStandards


def github_remote_url(repo: Repo) -> str:
    return f"https://github.com/{repo}.git"


async def run(request: RunRequest, services: Services) -> PullRequest:
    """Meets FR-1. Hands back the run's PR.

    Raises RunRefusedError when the run doesn't start, RunEndedError when it ends
    without a PR, and OpenedPullRequestError when it ends after opening one.
    """
    setup = await set_up(request, services)
    try:
        issue = await read_issue(services.graphql, request.repo, request.issue_number)
    except GitHubError as error:
        raise RunRefusedError(str(error)) from error
    try:
        await move_issue(services.graphql, request.repo, issue, Moment.RUN_STARTED)
        return await work_to_pull_request(request, services, setup, issue)
    except OpenedPullRequestError:
        raise
    except RUN_ENDING_ERRORS as error:
        raise await end_run(request, services, issue, str(error)) from error
    except Exception as error:
        reason = f"The workflow failed with an error it doesn't handle: {error!r}"
        await end_run(request, services, issue, reason)
        raise


async def set_up(request: RunRequest, services: Services) -> Setup:
    """Gets the clones, the run's settings and its doc standards.

    All before anything changes on GitHub.
    """
    try:
        clone = await open_repo_clone(services, request.repo)
        settings_file = await read_settings_file(clone)
        settings = run_settings(settings_file, request.rounds)
        doc_standards = await open_doc_standards(request, services)
    except (GitError, SettingsError, DocStandardsError) as error:
        raise RunRefusedError(str(error)) from error
    return Setup(clone, settings, doc_standards)


async def open_repo_clone(services: Services, repo: Repo) -> Clone:
    path = services.home / "clones" / repo.owner / repo.name
    return await open_clone(services.remote_url(repo), path)


async def open_doc_standards(request: RunRequest, services: Services) -> DocStandards:
    """Meets FR-32 and FR-33."""
    source = factory_config().doc_standards
    clone = await open_repo_clone(services, Repo.parse(source.repo))
    return await find_doc_standards(
        clone, request.doc_standards_branch or source.branch
    )


async def read_settings_file(clone: Clone) -> str | None:
    try:
        return await default_branch_file(clone, SETTINGS_FILE)
    except UnicodeDecodeError as error:
        message = f"The project's {SETTINGS_FILE} isn't UTF-8 text: {error}"
        raise SettingsError(message) from error


async def work_to_pull_request(
    request: RunRequest,
    services: Services,
    setup: Setup,
    issue: Issue,
) -> PullRequest:
    branch = run_branch_name(request.issue_number, request.started_at)
    path = (
        services.home / "working-copies" / request.repo.owner / request.repo.name
    ) / branch.replace("/", "-")
    async with working_copy(
        setup.clone, issue.number, request.started_at, path
    ) as copy:
        await exclude_doc_standards(copy)
        await write_doc_standards(setup.doc_standards, copy.path)
        context = RunContext(
            issue, copy, setup.settings, setup.doc_standards, services.runner
        )
        record = await work_and_rounds(context)
        await push(copy)
    # Meets FR-15.
    return await open_pull_request(services.graphql, request.repo, record)


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
