import asyncio
from typing import TYPE_CHECKING

import pytest

from software_factory.roles.definition import EditGuard, edit_guard_hook, role_options
from software_factory.roles.implementer import IMPLEMENTER
from software_factory.roles.quality_reviewer import (
    UNCOMMITTED_CHANGES,
    quality_reviewer,
)

if TYPE_CHECKING:
    from pathlib import Path

    from claude_agent_sdk import HookJSONOutput, PreToolUseHookInput

GUARD = EditGuard(paths=("docs/standards", "tools/check-docs.sh"), reason="Leave it.")


def pre_tool_use(tool_name: str, file_path: str, cwd: Path) -> PreToolUseHookInput:
    return {
        "hook_event_name": "PreToolUse",
        "session_id": "session",
        "transcript_path": str(cwd / "transcript.jsonl"),
        "cwd": str(cwd),
        "tool_name": tool_name,
        "tool_input": {"file_path": file_path, "content": "Changed\n"},
        "tool_use_id": "tool-use",
    }


def decide(file_path: str, cwd: Path, tool_name: str = "Write") -> HookJSONOutput:
    hook = edit_guard_hook(GUARD, cwd)
    hook_input = pre_tool_use(tool_name, file_path, cwd)
    return asyncio.run(hook(hook_input, "tool-use", {"signal": None}))


@pytest.mark.parametrize(
    "file_path",
    [
        "docs/standards/README.md",
        "docs/../docs/standards/new.md",
        "tools/check-docs.sh",
        "{cwd}/docs/standards/specs.md",
    ],
)
def test_edit_guard_refuses_a_change_to_a_guarded_path(
    tmp_path: Path, file_path: str
) -> None:
    output = decide(file_path.format(cwd=tmp_path), tmp_path, "Edit")

    assert output == {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": "Leave it.",
        }
    }


@pytest.mark.parametrize(
    "file_path",
    ["docs/standards-notes.md", "docs/functional-spec.md", "tools/other.sh"],
)
def test_edit_guard_lets_other_changes_through(tmp_path: Path, file_path: str) -> None:
    assert decide(file_path, tmp_path) == {}


def test_only_the_implementer_has_an_edit_guard(tmp_path: Path) -> None:
    """Meets FR-35. The quality reviewer has no tool that changes a file."""
    implementer = role_options(IMPLEMENTER, tmp_path, session_id=None)
    reviewer = role_options(
        quality_reviewer(UNCOMMITTED_CHANGES), tmp_path, session_id=None
    )

    assert implementer.hooks is not None
    [matcher] = implementer.hooks["PreToolUse"]
    assert matcher.matcher == "Edit|Write"
    assert reviewer.hooks is None
