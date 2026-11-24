"""The test that calls Claude (CS-4). Run it with `uv run pytest -m claude src`.

It checks what the fake Agent SDK takes for granted, on Haiku to keep it cheap.
"""

import asyncio
from typing import TYPE_CHECKING

import pytest
from claude_agent_sdk import query

from software_factory.roles.definition import ResultModel, RoleDefinition
from software_factory.roles.run import RoleRunner

if TYPE_CHECKING:
    from pathlib import Path


class CodeWords(ResultModel):
    project_code_word: str
    parent_code_word: str


ROLE = RoleDefinition(
    name="test role",
    model="claude-haiku-5-5",
    effort="low",
    prompt="You are a test role. Answer from your context, without tools.",
    tools=("Read",),
    turn_cap=5,
    result_model=CodeWords,
)

ASK = (
    "What code words does your context give, from each CLAUDE.md you were given?"
    " Put the project's in project_code_word, and the parent folder's in"
    " parent_code_word. Use NONE for one that isn't there."
)


@pytest.mark.claude
def test_role_starts_and_resumes_with_a_result(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("The parent folder's code word is OTTER.\n")
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "CLAUDE.md").write_text("The project's code word is PELICAN.\n")
    runner = RoleRunner(query)

    async def start_and_resume() -> tuple[str, str]:
        started = await runner.start(ROLE, ASK, repo)
        assert started.result == CodeWords(
            project_code_word="PELICAN", parent_code_word="NONE"
        )
        resumed = await runner.resume(
            started, ROLE, "Hand back the same answer again.", repo
        )
        assert resumed.result == started.result
        return started.session_id, resumed.session_id

    started_session, resumed_session = asyncio.run(start_and_resume())

    assert resumed_session == started_session
