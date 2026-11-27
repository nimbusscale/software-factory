"""The run folder's list of each time the workflow started or resumed a role (FR-41)."""

from typing import TYPE_CHECKING

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    TypeAdapter,
    ValidationError,
)

if TYPE_CHECKING:
    from pathlib import Path


class ModelUse(BaseModel):
    """What one model used in one start or resume of a role (FR-46).

    Read from the `modelUsage` in Claude Code's result, by its names, which holds more
    keys than these. Written to the list, and read back, by the names here.
    """

    model_config = ConfigDict(
        frozen=True, validate_by_alias=True, validate_by_name=True
    )

    input_tokens: int = Field(alias="inputTokens")
    output_tokens: int = Field(alias="outputTokens")
    cache_read_input_tokens: int = Field(alias="cacheReadInputTokens")
    cache_creation_input_tokens: int = Field(alias="cacheCreationInputTokens")
    web_search_requests: int = Field(alias="webSearchRequests")
    cost_usd: float = Field(alias="costUSD")


MODEL_USES = TypeAdapter(dict[str, ModelUse])


class AgentListEntry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    agent: str
    resumed: bool
    # The transcript is `<session_id>.jsonl`, in the run folder's transcripts. None when
    # the role stopped before Claude Code sent its result.
    session_id: str | None
    # The result's subtype, such as `success` or `error_max_turns`, or `no_result`.
    ended: str
    error: str | None
    turns: int | None
    # Claude Code gives a resumed session's cost and tokens as the session's totals so
    # far, not the resume's own, so each line's `cost_usd` and `models` include the
    # lines before it for the same session.
    cost_usd: float | None
    # Each model the role used, by the model's name. None when there's no result, when
    # the result's `modelUsage` doesn't fit `ModelUse`, or in a line without the field.
    models: dict[str, ModelUse] | None = None
    duration_ms: int | None
    result: JsonValue


def model_uses(model_usage: object) -> dict[str, ModelUse] | None:
    """The `modelUsage` in Claude Code's result, checked against `ModelUse` (TR-14).

    None when it doesn't fit, since a token count that's missing doesn't change the
    run's work, so it doesn't end the run.
    """
    try:
        return MODEL_USES.validate_python(model_usage)
    except ValidationError:
        return None


def add_entry(agent_list: Path, entry: AgentListEntry) -> None:
    """Adds the entry to the end of the list, one JSON object a line.

    One line for each role as it ends, so a run that stops partway keeps the entries
    for the roles before it.
    """
    with agent_list.open("a", encoding="utf-8") as file:
        file.write(entry.model_dump_json() + "\n")
