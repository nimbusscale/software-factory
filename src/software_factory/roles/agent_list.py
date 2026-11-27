"""The run folder's list of each time the workflow started or resumed a role (FR-41)."""

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, JsonValue

if TYPE_CHECKING:
    from pathlib import Path


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
    cost_usd: float | None
    duration_ms: int | None
    result: JsonValue


def add_entry(agent_list: Path, entry: AgentListEntry) -> None:
    """Adds the entry to the end of the list, one JSON object a line.

    One line for each role as it ends, so a run that stops partway keeps the entries
    for the roles before it.
    """
    with agent_list.open("a", encoding="utf-8") as file:
        file.write(entry.model_dump_json() + "\n")
