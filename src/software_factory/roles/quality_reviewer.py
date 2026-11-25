from typing import Literal

from software_factory.config import factory_config
from software_factory.roles.definition import (
    OPUS,
    ResultModel,
    RoleDefinition,
    read_prompt,
)

REVIEW_TARGET_PLACEHOLDER = "{{review_target}}"

# The review target the workflow names, since the review diff is the review copy's
# changes not yet committed (TD-2). The prompt names this target where it gives the
# git command for it, so the words have to match.
UNCOMMITTED_CHANGES = "the changes not yet committed"


class Finding(ResultModel):
    file: str
    line: int
    label: str
    # Meets FR-27.
    mark: Literal["important", "pre_existing", "nit", "to_check"]
    problem: str
    failure_case: str
    label_reason: str


class DroppedCandidate(ResultModel):
    file: str
    line: int
    problem: str
    label: str
    dropped_as: Literal["false_claim", "older_note", "earlier_finding"]
    reason: str


class QualityReviewerResult(ResultModel):
    status: Literal["done", "stopped"]
    reason: str
    findings: list[Finding]
    dropped: list[DroppedCandidate]


def stopped_reason(result: QualityReviewerResult) -> str | None:
    if result.status == "stopped":
        return f"The quality reviewer couldn't get the review diff: {result.reason}"
    return None


def quality_reviewer_prompt(review_target: str) -> str:
    return fill_review_target(read_prompt("quality-reviewer.md"), review_target)


def fill_review_target(template: str, review_target: str) -> str:
    if template.count(REVIEW_TARGET_PLACEHOLDER) != 1:
        message = (
            f"The quality reviewer's prompt needs {REVIEW_TARGET_PLACEHOLDER} once."
        )
        raise ValueError(message)
    return template.replace(REVIEW_TARGET_PLACEHOLDER, review_target)


def quality_reviewer(review_target: str) -> RoleDefinition[QualityReviewerResult]:
    return RoleDefinition(
        name="quality reviewer",
        model=OPUS,
        effort="high",
        prompt=quality_reviewer_prompt(review_target),
        # No tool that edits, since the reviewer only reads and reports.
        tools=("Read", "Glob", "Grep", "Bash"),
        turn_cap=factory_config().settings.turn_caps.quality_reviewer,
        result_model=QualityReviewerResult,
        ends_run=stopped_reason,
    )
