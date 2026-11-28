"""The review command's review of one PR (FR-47)."""

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from software_factory.git.command import GitError
from software_factory.git.pull_request_clone import pull_request_clone
from software_factory.git.review_copy import review_copy
from software_factory.github.api import GitHubError
from software_factory.github.issue import post_comment
from software_factory.github.pull_request import findings_comment, transcripts_line
from software_factory.loop.contract import ContractError, make
from software_factory.loop.messages import findings_message, reviewer_message
from software_factory.loop.rounds import findings_to_give, numbered
from software_factory.loop.settings import (
    SettingsError,
    project_settings,
    settings_file_at,
)
from software_factory.review.pull_request import read_pull_request
from software_factory.roles.quality_reviewer import (
    UNCOMMITTED_CHANGES,
    quality_reviewer,
)
from software_factory.roles.run import RoleFailedError

if TYPE_CHECKING:
    from collections.abc import Callable

    from software_factory.git.pull_request_clone import PullRequestClone
    from software_factory.git.working_copy import Remote
    from software_factory.github.api import GraphQL, Repo
    from software_factory.github.pull_request import NumberedFinding
    from software_factory.review.pull_request import PullRequestToReview
    from software_factory.roles.quality_reviewer import QualityReviewerResult
    from software_factory.roles.run import RoleRunner

# The errors that end the review command with a reason for the owner.
REVIEW_ENDING_ERRORS = (
    GitHubError,
    GitError,
    ContractError,
    SettingsError,
    RoleFailedError,
)

NOTHING_TO_FIX = (
    "The quality reviewer reported no important finding, so there's nothing to fix."
)


class ReviewEndedError(Exception):
    """The review command ended without a review. The message says why."""


@dataclass(frozen=True)
class ReviewRequest:
    repo: Repo
    pull_request_number: int


@dataclass(frozen=True)
class ReviewServices:
    graphql: GraphQL
    runner: RoleRunner
    remote: Callable[[Repo], Remote]
    factory_version: str
    # The run folder's name.
    run_folder: str


@dataclass(frozen=True)
class Review:
    pull_request: PullRequestToReview
    # The findings FR-23 would give the implementer (FR-48).
    given: list[NumberedFinding]
    # The comment the review command posts on the PR (FR-49).
    comment: str
    # Why the comment couldn't be posted, or None when it was.
    comment_error: str | None = None

    def printed(self) -> str:
        """What the review command prints for the PR's author (FR-48)."""
        answer = findings_message(self.given) if self.given else f"{NOTHING_TO_FIX}\n"
        if self.comment_error is None:
            return (
                f"{answer}\nThe rest of the review is in a comment on the PR,"
                f" {self.pull_request.url}\n"
            )
        # The review took minutes, so its findings are kept even when GitHub fails.
        return (
            f"{answer}\nThe rest of the review couldn't be posted on the PR:"
            f" {self.comment_error}\n\nHere it is instead:\n\n{self.comment}"
        )


async def review_pull_request(
    request: ReviewRequest, services: ReviewServices
) -> Review:
    """Reviews the PR and posts the review's comment on it.

    Raises ReviewEndedError when the review command ends without a review.
    """
    try:
        pull_request = await read_pull_request(
            services.graphql, request.repo, request.pull_request_number
        )
        async with pull_request_clone(
            services.remote(request.repo),
            pull_request.number,
            pull_request.base_ref_name,
        ) as clone:
            if clone.diff.start == clone.diff.end:
                message = (
                    "The PR has no changes since its head branched off its base"
                    " branch, such as a PR that's already merged. So there's nothing"
                    " to review."
                )
                raise ReviewEndedError(message)
            result = await review_clone(clone, pull_request, services.runner)
            head = clone.diff.end
    except REVIEW_ENDING_ERRORS as error:
        raise ReviewEndedError(str(error)) from error
    # The IDs of a run's first round, so the comment and the printed findings
    # name each finding the way a run's would (TD-12).
    findings = numbered(1, result.findings)
    given = findings_to_give(findings)
    comment = (
        f"The factory's quality reviewer reviewed this PR at `{head}`.\n\n"
        + findings_comment(
            findings,
            {n.finding_id for n in given},
            result.dropped,
            author="the PR's author",
        )
        + f"\nReviewed by factory version `{services.factory_version}`."
        f" {transcripts_line(services.run_folder)}\n"
    )
    review = Review(pull_request=pull_request, given=given, comment=comment)
    try:
        # Meets FR-49.
        await post_comment(services.graphql, pull_request.id, comment)
    except GitHubError as error:
        return replace(review, comment_error=str(error))
    return review


async def review_clone(
    clone: PullRequestClone, pull_request: PullRequestToReview, runner: RoleRunner
) -> QualityReviewerResult:
    """Runs the quality reviewer on the PR's review diff, in a review copy."""
    # From where the head branched off, so the PR's own changes don't set how it's
    # reviewed.
    settings = project_settings(await settings_file_at(clone.path, clone.diff.start))
    reviewer = replace(
        quality_reviewer(UNCOMMITTED_CHANGES),
        turn_cap=settings.turn_caps.quality_reviewer,
    )
    # Meets TR-26: no earlier findings, as in a run's first round.
    message = reviewer_message(pull_request.issue_body(), [], (), ())
    async with review_copy(clone.path, clone.diff) as path:
        # Meets TR-23, and TR-27 through the error it raises when it fails.
        await make("setup", path, "the review copy")
        outcome = await runner.start(reviewer, message, path)
    return outcome.result
