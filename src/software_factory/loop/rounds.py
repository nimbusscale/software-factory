from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING

from software_factory.git.review_copy import ReviewDiff, review_copy, review_diff
from software_factory.git.working_copy import commit
from software_factory.github.pull_request import NumberedFinding, RunRecord
from software_factory.loop.contract import make
from software_factory.loop.messages import findings_message, reviewer_message
from software_factory.roles.implementer import IMPLEMENTER
from software_factory.roles.quality_reviewer import (
    UNCOMMITTED_CHANGES,
    quality_reviewer,
)

if TYPE_CHECKING:
    from software_factory.config import Settings
    from software_factory.git.working_copy import WorkingCopy
    from software_factory.github.issue import Issue
    from software_factory.roles.implementer import DeclinedFinding
    from software_factory.roles.quality_reviewer import DroppedCandidate
    from software_factory.roles.run import RoleRunner


class NothingToReviewError(Exception):
    """The implementer's work changed no file, so the run ends."""


@dataclass(frozen=True)
class RunContext:
    issue: Issue
    working_copy: WorkingCopy
    settings: Settings
    runner: RoleRunner
    # The run folder's name.
    run_folder: str


@dataclass
class Kept:
    """What a run keeps from its rounds, for the reviews after them and for its PR."""

    findings: list[NumberedFinding] = field(default_factory=list)
    dropped: list[DroppedCandidate] = field(default_factory=list)
    # From every one of the implementer's results (TD-5).
    declined: list[DeclinedFinding] = field(default_factory=list)
    # The IDs of the findings the workflow gave the implementer.
    given: set[str] = field(default_factory=set)


async def work_and_rounds(context: RunContext) -> RunRecord:
    """Runs the implementer on the issue (FR-2), then the rounds.

    Commits each of the implementer's results (TD-8).
    """
    implementer = replace(IMPLEMENTER, turn_cap=context.settings.turn_caps.implementer)
    copy = context.working_copy
    outcome = await context.runner.start(implementer, context.issue.body, copy.path)
    kept = Kept()
    kept.declined.extend(outcome.result.declined)
    if await commit(copy, outcome.result.commit_message) is None:
        message = "The implementer handed back its result without changing any file."
        raise NothingToReviewError(message)
    diff: ReviewDiff | None = None
    # Meets FR-8 and FR-10.
    for round_number in range(1, context.settings.rounds + 1):
        diff = await review_diff(copy, diff)
        findings = await review(context, round_number, diff, kept)
        # Meets FR-24.
        if not any(n.finding.mark == "important" for n in findings):
            break
        # Meets FR-23.
        given = [n for n in findings if n.finding.mark in {"important", "nit"}]
        kept.given.update(n.finding_id for n in given)
        outcome = await context.runner.resume(
            outcome, implementer, findings_message(given), copy.path
        )
        kept.declined.extend(outcome.result.declined)
        # Meets TR-5.
        if await commit(copy, outcome.result.commit_message) is None:
            break
    return RunRecord(
        issue=context.issue,
        run_branch=copy.run_branch,
        run_folder=context.run_folder,
        last_result=outcome.result,
        declined=kept.declined,
        findings=kept.findings,
        given=frozenset(kept.given),
        dropped=kept.dropped,
    )


async def review(
    context: RunContext, round_number: int, diff: ReviewDiff, kept: Kept
) -> list[NumberedFinding]:
    """Runs the round's review, and keeps its findings and dropped candidates."""
    reviewer = replace(
        quality_reviewer(UNCOMMITTED_CHANGES),
        turn_cap=context.settings.turn_caps.quality_reviewer,
    )
    declined_ids = {declined.finding_id for declined in kept.declined}
    message = reviewer_message(
        context.issue.body, kept.findings, declined_ids, kept.given
    )
    async with review_copy(context.working_copy, diff) as path:
        # Meets TR-23, and TR-24 through the error it raises when it fails.
        await make("setup", path, "the review copy")
        outcome = await context.runner.start(reviewer, message, path)
    # Meets TD-12.
    findings = [
        NumberedFinding(finding_id=f"R{round_number}-F{place}", finding=finding)
        for place, finding in enumerate(outcome.result.findings, start=1)
    ]
    kept.findings.extend(findings)
    kept.dropped.extend(outcome.result.dropped)
    return findings
