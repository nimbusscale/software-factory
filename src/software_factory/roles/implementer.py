from pydantic import Field

from software_factory.roles.definition import (
    DEFAULT_TURN_CAP,
    OPUS,
    ResultModel,
    RoleDefinition,
    read_prompt,
)

# Each description below goes in the result schema, which the implementer sees as the
# StructuredOutput tool's input schema. The prompt says how the workflow uses the
# result.


class DeclinedFinding(ResultModel):
    finding_id: str = Field(
        description="The finding's ID, as the message gave it, such as `R1-F2`."
    )
    reason: str = Field(description="Why you declined it.")


class DocCodeDisagreement(ResultModel):
    item_id: str = Field(description="The doc item's ID, such as `TR-6`.")
    code: str = Field(description="Where the code is, such as a file and a function.")
    disagreement: str = Field(description="What the doc says, and what the code does.")


class Decision(ResultModel):
    text: str = Field(description="The text of the issue or doc it's about, quoted.")
    unclear: str = Field(description="What the text left unclear.")
    decision: str = Field(description="What you decided, and why.")


class MissingReason(ResultModel):
    decision: str = Field(description="The decision, quoted from the spec.")
    suggested_reason: str | None = Field(
        description="The reason you'd suggest, or null when you have none."
    )


class ImplementerResult(ResultModel):
    summary: str = Field(
        description=(
            "What your change does, in a few plain sentences, for someone skimming the"
            " project's PRs. Covers your whole change so far."
        )
    )
    declined: list[DeclinedFinding] = Field(
        description=(
            "Each finding in the last message you got that you declined. Covers only"
            " that message. Empty for your first result, and when you fixed every"
            " finding."
        )
    )
    disagreements: list[DocCodeDisagreement] = Field(
        description=(
            "Each place where a doc and the code say different things and your change"
            " leaves both as they are, such as one outside the issue's scope. Covers"
            " your whole change so far."
        )
    )
    decisions: list[Decision] = Field(
        description=(
            "Each decision you made on a point that neither the issue nor the docs"
            " settle. Covers your whole change so far, so leave out one that a later"
            " change undid."
        )
    )
    missing_reasons: list[MissingReason] = Field(
        description=(
            "Each decision you wrote into a spec with no Why, because neither the issue"
            " nor the docs give its reason. Covers your whole change so far."
        )
    )
    commit_message: str = Field(
        description=(
            "The message the workflow uses when it commits your changes. The commit"
            " holds the changes you made since your last result, or since the start"
            " for your first result. Follow the project's docs on commit messages. In"
            " the message, give the history of the change, such as what you tried and"
            " why you chose this way."
        )
    )


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
