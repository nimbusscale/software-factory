import json
from dataclasses import dataclass
from importlib.resources import files
from typing import TYPE_CHECKING

from claude_agent_sdk import ClaudeAgentOptions, EffortLevel, HookMatcher
from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from claude_agent_sdk import HookCallback, HookContext, HookInput, HookJSONOutput

OPUS = "claude-opus-5-5"

GLOB_CHARACTERS = frozenset("*?[]{}()!+@")

# Meets AD-7 for the shell, and TD-7 for commits.
DENIED_COMMANDS = ("Bash(gh:*)", "Bash(git push:*)", "Bash(git commit:*)")

ROLE_ENVIRONMENT = {
    # Empty, so the role's shell finds no GitHub token in its environment (AD-7).
    "GH_TOKEN": "",
    "GITHUB_TOKEN": "",
    # Claude Code's memory would carry notes from one run to the next (TR-11).
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


# The tools that change a file, which an EditGuard's hook runs before.
EDIT_TOOLS = ("Edit", "Write")


@dataclass(frozen=True)
class EditGuard:
    """Paths a role may read but not change with its tools that change a file."""

    # Files and folders, from the folder the role runs in.
    paths: tuple[str, ...]
    # What the role is told when its hook refuses a change.
    reason: str


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
    edit_guard: EditGuard | None = None


def read_prompt(file_name: str) -> str:
    prompt = files("software_factory") / "prompts" / file_name
    return prompt.read_text(encoding="utf-8")


def role_options[ResultT: ResultModel](
    definition: RoleDefinition[ResultT],
    cwd: Path,
    session_id: str | None,
) -> ClaudeAgentOptions:
    """The options a role starts with, or resumes with when `session_id` is given."""
    if GLOB_CHARACTERS & set(str(cwd)):
        # The folder goes into a glob in claudeMdExcludes below, unescaped.
        message = f"A role can't run in {cwd}, since its path has a glob character."
        raise ValueError(message)
    return ClaudeAgentOptions(
        model=definition.model,
        effort=definition.effort,
        # The roles are coding agents, so they keep Claude Code's own guidance on
        # its tools.
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": definition.prompt,
        },
        tools=list(definition.tools),
        allowed_tools=list(definition.tools),
        disallowed_tools=list(DENIED_COMMANDS),
        # Refuses each tool call the rules above don't allow, since no one is there
        # to ask.
        permission_mode="dontAsk",
        # Only the project's own settings and CLAUDE.md, which points the role to the
        # project's docs (AD-9).
        setting_sources=["project"],
        # Claude Code also loads each CLAUDE.md in the folders above the working
        # directory, such as ~/.claude/CLAUDE.md when the working copy is in the
        # home folder. This keeps only the ones in the role's own folder (TR-7,
        # TR-11).
        settings=json.dumps({"claudeMdExcludes": [f"!{cwd}/**"]}),
        env=ROLE_ENVIRONMENT,
        # The prompt holds text from GitHub, such as the issue's body. Without this,
        # an @path in it makes Claude Code read that file into the prompt (TR-11).
        verbatim_prompts=True,
        # Meets FR-6.
        max_turns=definition.turn_cap,
        # Meets TD-1 and TD-11.
        output_format={
            "type": "json_schema",
            "schema": definition.result_model.model_json_schema(),
        },
        hooks=(
            None
            if definition.edit_guard is None
            else {
                "PreToolUse": [
                    HookMatcher(
                        matcher="|".join(EDIT_TOOLS),
                        hooks=[edit_guard_hook(definition.edit_guard, cwd)],
                    )
                ]
            }
        ),
        cwd=cwd,
        resume=session_id,
    )


def edit_guard_hook(guard: EditGuard, cwd: Path) -> HookCallback:
    """A hook that refuses each change to a path the guard holds."""
    guarded = [(cwd / name).resolve() for name in guard.paths]

    async def hook(
        hook_input: HookInput, _tool_use_id: str | None, _context: HookContext
    ) -> HookJSONOutput:
        if hook_input["hook_event_name"] != "PreToolUse":
            return {}
        file_path = hook_input["tool_input"].get("file_path")
        if not isinstance(file_path, str):
            return {}
        # Resolved, so a path such as docs/../docs/standards is caught too.
        target = (cwd / file_path).resolve()
        if not any(target == path or path in target.parents for path in guarded):
            return {}
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": guard.reason,
            }
        }

    return hook
