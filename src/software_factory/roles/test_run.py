import asyncio
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from claude_agent_sdk import ClaudeAgentOptions, Message, query

from software_factory.roles.agent_list import AgentListEntry
from software_factory.roles.definition import ResultModel, RoleDefinition
from software_factory.roles.fake_agent_sdk import (
    FakeQuery,
    RawMessage,
    ReplayTransport,
    result_message,
    saved_response,
)
from software_factory.roles.implementer import IMPLEMENTER, ImplementerResult
from software_factory.roles.quality_reviewer import (
    UNCOMMITTED_CHANGES,
    quality_reviewer,
)
from software_factory.roles.run import RoleFailedError, RoleOutcome, RoleRunner

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from pydantic import JsonValue

WORKING_COPY = Path("/work/copy")

IMPLEMENTER_RESULT: dict[str, JsonValue] = {
    "summary": "Adds the trip length check.",
    "declined": [],
    "disagreements": [],
    "decisions": [],
    "missing_reasons": [],
    "commit_message": "Check the trip length",
}


def start[ResultT: ResultModel](
    definition: RoleDefinition[ResultT], messages: list[RawMessage]
) -> RoleOutcome[ResultT]:
    runner = RoleRunner(FakeQuery([messages]))
    return asyncio.run(runner.start(definition, "Do the work.", WORKING_COPY))


def test_hands_back_the_result_and_session() -> None:
    outcome = start(
        IMPLEMENTER,
        [result_message(structured_output=IMPLEMENTER_RESULT, session_id="s-1")],
    )

    assert outcome.result == ImplementerResult.model_validate(IMPLEMENTER_RESULT)
    assert outcome.session_id == "s-1"


def test_success_without_structured_output_ends_the_run() -> None:
    with pytest.raises(RoleFailedError, match="without handing back a result"):
        start(IMPLEMENTER, saved_response("success_without_structured_output"))


def test_turn_cap_reached_ends_the_run() -> None:
    with pytest.raises(RoleFailedError, match="reached its turn cap of 100 turns"):
        start(IMPLEMENTER, saved_response("turn_cap_reached"))


def test_result_that_doesnt_fit_its_schema_ends_the_run() -> None:
    result: JsonValue = {**IMPLEMENTER_RESULT, "declined": [{"finding_id": "R1-F1"}]}

    with pytest.raises(RoleFailedError, match="doesn't fit its result schema"):
        start(IMPLEMENTER, [result_message(structured_output=result)])


def test_result_with_a_field_the_schema_lacks_ends_the_run() -> None:
    result: JsonValue = {**IMPLEMENTER_RESULT, "notes": "extra"}

    with pytest.raises(RoleFailedError, match="doesn't fit its result schema"):
        start(IMPLEMENTER, [result_message(structured_output=result)])


def test_error_result_ends_the_run() -> None:
    error = result_message(
        subtype="error_during_execution", is_error=True, errors=["API error"]
    )

    with pytest.raises(RoleFailedError, match="stopped with an error: API error"):
        start(IMPLEMENTER, [error])


def test_no_result_message_ends_the_run() -> None:
    with pytest.raises(RoleFailedError, match="ended without a result"):
        start(IMPLEMENTER, [])


def test_quality_reviewer_that_stopped_ends_the_run() -> None:
    stopped: JsonValue = {
        "status": "stopped",
        "reason": "git diff printed: not a git repository.",
        "findings": [],
        "dropped": [],
    }

    with pytest.raises(RoleFailedError, match="not a git repository"):
        start(
            quality_reviewer(UNCOMMITTED_CHANGES),
            [result_message(structured_output=stopped)],
        )


def test_start_uses_a_new_session_and_resume_the_same_one() -> None:
    fake = FakeQuery(
        [
            [result_message(structured_output=IMPLEMENTER_RESULT, session_id="s-1")],
            [result_message(structured_output=IMPLEMENTER_RESULT, session_id="s-1")],
        ]
    )
    runner = RoleRunner(fake)

    async def start_and_resume() -> None:
        outcome = await runner.start(IMPLEMENTER, "Do the work.", WORKING_COPY)
        await runner.resume(outcome, IMPLEMENTER, "Findings: F1.", WORKING_COPY)

    asyncio.run(start_and_resume())

    assert [options.resume for options in fake.options] == [None, "s-1"]


def listed(agent_list: Path) -> list[AgentListEntry]:
    lines = agent_list.read_text(encoding="utf-8").splitlines()
    return [AgentListEntry.model_validate_json(line) for line in lines]


def test_lists_each_start_and_resume_in_order(tmp_path: Path) -> None:
    agent_list = tmp_path / "agents.jsonl"
    fake = FakeQuery(
        [
            [result_message(structured_output=IMPLEMENTER_RESULT, session_id="s-1")],
            [
                result_message(
                    structured_output=IMPLEMENTER_RESULT,
                    session_id="s-1",
                    num_turns=4,
                    total_cost_usd=0.25,
                )
            ],
        ]
    )
    runner = RoleRunner(fake, agent_list=agent_list)

    async def start_and_resume() -> None:
        outcome = await runner.start(IMPLEMENTER, "Do the work.", WORKING_COPY)
        await runner.resume(outcome, IMPLEMENTER, "Findings: F1.", WORKING_COPY)

    asyncio.run(start_and_resume())

    started, resumed = listed(agent_list)
    # FR-41.
    assert (started.agent, started.resumed) == ("implementer", False)
    assert (resumed.agent, resumed.resumed) == ("implementer", True)
    assert resumed.session_id == "s-1"
    assert (resumed.ended, resumed.error) == ("success", None)
    assert (resumed.turns, resumed.cost_usd) == (4, 0.25)
    assert resumed.result == IMPLEMENTER_RESULT


def test_lists_a_role_that_ends_the_run(tmp_path: Path) -> None:
    agent_list = tmp_path / "agents.jsonl"
    runner = RoleRunner(
        FakeQuery([saved_response("turn_cap_reached"), []]), agent_list=agent_list
    )

    with pytest.raises(RoleFailedError):
        asyncio.run(runner.start(IMPLEMENTER, "Do the work.", WORKING_COPY))
    with pytest.raises(RoleFailedError):
        asyncio.run(runner.start(IMPLEMENTER, "Do the work.", WORKING_COPY))

    at_turn_cap, no_result = listed(agent_list)
    # FR-41.
    assert at_turn_cap.ended == "error_max_turns"
    assert at_turn_cap.session_id is not None
    assert (no_result.ended, no_result.session_id) == ("no_result", None)


def test_gives_the_role_its_turn_cap_each_time() -> None:
    implementer = replace(IMPLEMENTER, turn_cap=7)
    fake = FakeQuery(
        [
            [result_message(structured_output=IMPLEMENTER_RESULT)],
            [result_message(structured_output=IMPLEMENTER_RESULT)],
        ]
    )
    runner = RoleRunner(fake)

    async def start_and_resume() -> None:
        outcome = await runner.start(implementer, "Do the work.", WORKING_COPY)
        await runner.resume(outcome, implementer, "Findings: F1.", WORKING_COPY)

    asyncio.run(start_and_resume())

    assert [options.max_turns for options in fake.options] == [7, 7]


def test_gives_the_role_its_result_schema() -> None:
    fake = FakeQuery([[result_message(structured_output=IMPLEMENTER_RESULT)]])

    asyncio.run(RoleRunner(fake).start(IMPLEMENTER, "Do the work.", WORKING_COPY))

    assert fake.options[0].output_format == {
        "type": "json_schema",
        "schema": ImplementerResult.model_json_schema(),
    }


def test_api_failure_gives_the_text_claude_code_sent() -> None:
    failure = result_message(
        is_error=True, errors=[], result="API Error: 529 Overloaded"
    )

    with pytest.raises(RoleFailedError, match="API Error: 529 Overloaded"):
        start(IMPLEMENTER, [failure])


def test_sdk_error_after_a_success_result_ends_the_run() -> None:
    def crashing_query(
        *, prompt: str, options: ClaudeAgentOptions
    ) -> AsyncIterator[Message]:
        success = result_message(structured_output=IMPLEMENTER_RESULT)
        transport = ReplayTransport([success], exit_code=2)
        return query(prompt=prompt, options=options, transport=transport)

    runner = RoleRunner(crashing_query)

    with pytest.raises(RoleFailedError, match="exit code 2"):
        asyncio.run(runner.start(IMPLEMENTER, "Do the work.", WORKING_COPY))


@pytest.mark.parametrize(
    "definition", [IMPLEMENTER, quality_reviewer(UNCOMMITTED_CHANGES)]
)
def test_role_loads_no_settings_and_gets_no_github_token(
    definition: RoleDefinition[ResultModel],
) -> None:
    fake = FakeQuery([[]])

    with pytest.raises(RoleFailedError):
        asyncio.run(RoleRunner(fake).start(definition, "Do the work.", WORKING_COPY))

    [options] = fake.options
    # AD-13.
    assert options.setting_sources == []
    # AD-7.
    assert options.env["GH_TOKEN"] == options.env["GITHUB_TOKEN"] == ""


@pytest.mark.parametrize(
    "definition", [IMPLEMENTER, quality_reviewer(UNCOMMITTED_CHANGES)]
)
def test_role_gets_the_factory_plugin_and_only_its_standards_skill(
    definition: RoleDefinition[ResultModel],
) -> None:
    fake = FakeQuery([[]])

    with pytest.raises(RoleFailedError):
        asyncio.run(RoleRunner(fake).start(definition, "Do the work.", WORKING_COPY))

    [options] = fake.options
    # AD-14.
    assert options.plugins == [{"type": "local", "path": "/factory/plugin"}]
    assert "Skill" in (options.tools or [])
    # AD-13.
    assert options.skills == ["software-factory:standards"]
    skill_rules = [rule for rule in options.allowed_tools if rule.startswith("Skill")]
    assert skill_rules == ["Skill(software-factory:standards)"]
