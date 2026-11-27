from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from claude_agent_sdk import ClaudeAgentOptions, ClaudeSDKError, Message, ResultMessage
from pydantic import ValidationError

from software_factory.roles.agent_list import AgentListEntry, add_entry
from software_factory.roles.definition import ResultModel, RoleDefinition, role_options

if TYPE_CHECKING:
    from collections.abc import AsyncIterator
    from pathlib import Path


class Query(Protocol):
    """The Agent SDK's `query`, or a fake of it in tests."""

    def __call__(
        self, *, prompt: str, options: ClaudeAgentOptions
    ) -> AsyncIterator[Message]: ...


class RoleFailedError(Exception):
    """A role's result, or the lack of one, ends the run (TR-2, FR-7).

    The message says why, in words for the owner, who reads it in the issue's comment.
    """


@dataclass(frozen=True)
class RoleOutcome[ResultT: ResultModel]:
    result: ResultT
    session_id: str


class RoleRunner:
    def __init__(self, query: Query, agent_list: Path | None = None) -> None:
        """`agent_list` is the run folder's list of roles, or None to keep no list."""
        self._query = query
        self._agent_list = agent_list

    async def start[ResultT: ResultModel](
        self, definition: RoleDefinition[ResultT], prompt: str, cwd: Path
    ) -> RoleOutcome[ResultT]:
        """Starts the role in a new session (TR-6)."""
        options = role_options(definition, cwd, session_id=None)
        return await self._run(definition, prompt, options, resumed=False)

    async def resume[ResultT: ResultModel](
        self,
        outcome: RoleOutcome[ResultT],
        definition: RoleDefinition[ResultT],
        prompt: str,
        cwd: Path,
    ) -> RoleOutcome[ResultT]:
        """Resumes the session that `outcome` came from (TD-3)."""
        options = role_options(definition, cwd, session_id=outcome.session_id)
        return await self._run(definition, prompt, options, resumed=True)

    async def _run[ResultT: ResultModel](
        self,
        definition: RoleDefinition[ResultT],
        prompt: str,
        options: ClaudeAgentOptions,
        *,
        resumed: bool,
    ) -> RoleOutcome[ResultT]:
        result_message: ResultMessage | None = None
        sdk_error: ClaudeSDKError | None = None
        try:
            async for message in self._query(prompt=prompt, options=options):
                if isinstance(message, ResultMessage):
                    result_message = message
        except ClaudeSDKError as error:
            sdk_error = error
        if self._agent_list is not None:
            entry = agent_list_entry(
                definition.name,
                resumed=resumed,
                result_message=result_message,
                sdk_error=sdk_error,
            )
            add_entry(self._agent_list, entry)
        # When a role ends with an error result, such as at its turn cap, the SDK
        # hands over the result message and then raises. The result message says
        # more than the error does.
        if sdk_error is not None and (
            result_message is None or not result_message.is_error
        ):
            reason = f"The {definition.name} stopped with an error: {sdk_error}"
            raise RoleFailedError(reason) from sdk_error
        if result_message is None:
            reason = f"The {definition.name} ended without a result."
            raise RoleFailedError(reason)
        return RoleOutcome(
            result=read_result(definition, result_message),
            session_id=result_message.session_id,
        )


def read_result[ResultT: ResultModel](
    definition: RoleDefinition[ResultT], result_message: ResultMessage
) -> ResultT:
    """Checks the role's result against its result schema (TR-1)."""
    name = definition.name
    if result_message.subtype == "error_max_turns":
        # Meets FR-7.
        message = f"The {name} reached its turn cap of {definition.turn_cap} turns."
        raise RoleFailedError(message)
    if result_message.is_error or result_message.subtype != "success":
        message = f"The {name} stopped with an error: {error_text(result_message)}"
        raise RoleFailedError(message)
    # The SDK reports success with no structured output when the role ends without
    # ever making a valid structured-output call. It nudges the role once to make
    # one, and the role can ignore the nudge. So success alone isn't a result.
    if result_message.structured_output is None:
        message = f"The {name} ended without handing back a result."
        raise RoleFailedError(message)
    try:
        result = definition.result_model.model_validate(
            result_message.structured_output
        )
    except ValidationError as error:
        message = f"The {name}'s result doesn't fit its result schema: {error}"
        raise RoleFailedError(message) from error
    reason = definition.ends_run(result)
    if reason is not None:
        raise RoleFailedError(reason)
    return result


def agent_list_entry(
    agent: str,
    *,
    resumed: bool,
    result_message: ResultMessage | None,
    sdk_error: ClaudeSDKError | None,
) -> AgentListEntry:
    if result_message is None:
        return AgentListEntry(
            agent=agent,
            resumed=resumed,
            session_id=None,
            ended="no_result",
            error=None if sdk_error is None else str(sdk_error),
            turns=None,
            cost_usd=None,
            duration_ms=None,
            result=None,
        )
    failed = result_message.is_error or result_message.subtype != "success"
    return AgentListEntry(
        agent=agent,
        resumed=resumed,
        session_id=result_message.session_id,
        ended=result_message.subtype,
        error=error_text(result_message) if failed else None,
        turns=result_message.num_turns,
        cost_usd=result_message.total_cost_usd,
        duration_ms=result_message.duration_ms,
        result=result_message.structured_output,
    )


def error_text(result_message: ResultMessage) -> str:
    if result_message.errors:
        return "; ".join(result_message.errors)
    # An API failure arrives with the subtype "success", no errors, and the text in
    # the result.
    if result_message.result and result_message.result.strip():
        return result_message.result.strip()
    return result_message.subtype
