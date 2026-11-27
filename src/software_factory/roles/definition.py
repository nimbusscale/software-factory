from dataclasses import dataclass
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING

from claude_agent_sdk import ClaudeAgentOptions, EffortLevel
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from collections.abc import Callable

OPUS = "claude-opus-5-5"

# The factory plugin in the SFE, from the same commit as this code (AD-14).
FACTORY_PLUGIN = Path("/factory/plugin")
STANDARDS_SKILL = "software-factory:standards"

# Meets AD-7 for the shell, and TD-7 for commits.
DENIED_COMMANDS = ("Bash(gh:*)", "Bash(git push:*)", "Bash(git commit:*)")

ROLE_ENVIRONMENT = {
    # Empty, so the role's shell finds no GitHub token in its environment (AD-7).
    "GH_TOKEN": "",
    "GITHUB_TOKEN": "",
    # Claude Code's memory would carry notes from one run to the next (TR-22).
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
}


class ResultModel(BaseModel):
    """A role's result schema (TD-10).

    Strict, so the check refuses what the JSON Schema the role gets refuses, such as a
    line number given as text (TD-11).
    """

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


def never_ends_run(_: BaseModel) -> str | None:
    return None


@dataclass(frozen=True)
class RoleDefinition[ResultT: ResultModel]:
    name: str
    model: str
    effort: EffortLevel
    prompt: str
    tools: tuple[str, ...]
    turn_cap: int
    result_model: type[ResultT]
    # Why a result that fits the schema still ends the run, or None when it doesn't.
    ends_run: Callable[[ResultT], str | None] = never_ends_run


def read_prompt(file_name: str) -> str:
    prompt = files("software_factory") / "prompts" / file_name
    return prompt.read_text(encoding="utf-8")


def role_options[ResultT: ResultModel](
    definition: RoleDefinition[ResultT],
    cwd: Path,
    session_id: str | None,
) -> ClaudeAgentOptions:
    """The options a role starts with, or resumes with when `session_id` is given."""
    return ClaudeAgentOptions(
        model=definition.model,
        effort=definition.effort,
        # Opus leaves the text of each thinking block out unless it's asked for. Without
        # it, a transcript shows what a role ran but not why, such as what a reviewer
        # suspected before a command settled it (FR-40).
        thinking={"type": "adaptive", "display": "summarized"},
        # The roles are coding agents, so they keep Claude Code's own guidance on
        # its tools.
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": definition.prompt,
        },
        tools=[*definition.tools, "Skill"],
        allowed_tools=[*definition.tools, f"Skill({STANDARDS_SKILL})"],
        disallowed_tools=list(DENIED_COMMANDS),
        # Refuses each tool call the rules above don't allow, since no one is there
        # to ask.
        permission_mode="dontAsk",
        # No settings file and no CLAUDE.md, the project's or any other, so a role's
        # instructions come only from its prompt and the factory plugin (AD-13).
        setting_sources=[],
        # Meets AD-14. Only the standards skill, since any other skill would give the
        # role instructions that aren't the factory's (AD-13).
        plugins=[{"type": "local", "path": str(FACTORY_PLUGIN)}],
        skills=[STANDARDS_SKILL],
        env=ROLE_ENVIRONMENT,
        # The prompt holds text from GitHub, such as the issue's body. Without this,
        # an @path in it makes Claude Code read that file into the prompt (TR-22).
        verbatim_prompts=True,
        # Meets FR-6.
        max_turns=definition.turn_cap,
        # Meets TD-1 and TD-11.
        output_format={
            "type": "json_schema",
            "schema": definition.result_model.model_json_schema(),
        },
        cwd=cwd,
        resume=session_id,
    )
