from software_factory.roles.definition import (
    DEFAULT_TURN_CAP,
    OPUS,
    ResultModel,
    RoleDefinition,
    read_prompt,
)


class DeclinedFinding(ResultModel):
    finding_id: str
    reason: str


class DocCodeDisagreement(ResultModel):
    item_id: str
    code: str
    disagreement: str


class OpenPointChoice(ResultModel):
    text: str
    unclear: str
    choice: str


class DecisionWithNoReason(ResultModel):
    decision: str
    suggested_reason: str | None


class ImplementerResult(ResultModel):
    summary: str
    declined: list[DeclinedFinding]
    disagreements: list[DocCodeDisagreement]
    choices: list[OpenPointChoice]
    decisions_with_no_reason: list[DecisionWithNoReason]
    commit_message: str


IMPLEMENTER = RoleDefinition(
    name="implementer",
    model=OPUS,
    effort="high",
    prompt=read_prompt("implementer.md"),
    # Meets TR-11.
    tools=("Read", "Glob", "Grep", "Edit", "Write", "Bash", "WebSearch", "WebFetch"),
    turn_cap=DEFAULT_TURN_CAP,
    result_model=ImplementerResult,
)
