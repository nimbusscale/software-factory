"""Each role's view file, which shows what the role is given (CS-6).

Rewrite the files with `uv run write-role-views`.
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING

from software_factory.roles.definition import (
    DEFAULT_TURN_CAP,
    ResultModel,
    RoleDefinition,
    role_options,
)
from software_factory.roles.implementer import IMPLEMENTER
from software_factory.roles.quality_reviewer import (
    UNCOMMITTED_CHANGES,
    quality_reviewer,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

VIEWS_FOLDER = Path(__file__).parent

# Stands for the working copy or review copy, since a role runs in a new folder each
# time.
ROLE_FOLDER = Path("/role-folder")


def role_views() -> dict[str, str]:
    """Each view file's name, and the text it should hold."""
    return {
        "implementer.view.md": role_view(IMPLEMENTER),
        "quality-reviewer.view.md": role_view(quality_reviewer(UNCOMMITTED_CHANGES)),
    }


def role_view[ResultT: ResultModel](definition: RoleDefinition[ResultT]) -> str:
    options = role_options(definition, ROLE_FOLDER, session_id=None)
    turn_cap = f"{options.max_turns} turns"
    if options.max_turns == DEFAULT_TURN_CAP:
        turn_cap += ", the factory's default"
    schema = json.dumps(options.output_format, indent=2)
    lines = [
        f"# What the {definition.name} is given",
        "",
        (
            "Written by `uv run write-role-views`, from the options the role starts"
            " with. Don't edit it by hand."
        ),
        "",
        f"Model: `{options.model}`. Effort: `{options.effort}`. Turn cap: {turn_cap}.",
        "",
        "## Tools",
        "",
        code_list(options.tools if isinstance(options.tools, list) else []),
        "",
        "## Permission rules",
        "",
        f"- Permission mode: `{options.permission_mode}`.",
        f"- Allowed: {code_list(options.allowed_tools)}.",
        f"- Denied: {code_list(options.disallowed_tools)}.",
        "",
        "## Settings",
        "",
        f"`{ROLE_FOLDER}` stands for the folder the role runs in.",
        "",
        f"- Setting sources: {code_list(options.setting_sources or [])}.",
        f"- Settings: `{options.settings}`.",
        f"- Environment: {code_list(f'{k}={v}' for k, v in options.env.items())}.",
        f"- Verbatim prompts: {'on' if options.verbatim_prompts else 'off'}.",
        "",
        "## System prompt",
        "",
        "Claude Code's own system prompt, with this added at its end:",
        "",
        "````text",
        definition.prompt.rstrip("\n"),
        "````",
        "",
        "## Output format",
        "",
        "```json",
        schema,
        "```",
        "",
    ]
    return "\n".join(lines)


def code_list(items: Iterable[str]) -> str:
    return ", ".join(f"`{item}`" for item in items)


def main() -> None:
    for file_name, text in role_views().items():
        (VIEWS_FOLDER / file_name).write_text(text, encoding="utf-8")
