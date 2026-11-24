"""Spike: can a role started from the Agent SDK run Claude Code's stock code review on the
changes not yet committed, and still hand back its findings as structured output?

Setup, in this folder:
  uv venv .venv && uv pip install --python .venv/bin/python claude-agent-sdk jsonschema
  bash make-template.sh

Usage: env -u CLAUDECODE .venv/bin/python spike.py <case>
  init   - list the skills, slash commands and tools a role gets (no review)
  slash  - the prompt is only "/code-review", with the findings schema
  told   - the prompt tells the role in words to run the stock code review, then hand back findings
Each run copies template/ to a fresh folder under runs/, and appends a record to results.jsonl.
"""

import asyncio
import json
import shutil
import sys
import time
from pathlib import Path

import jsonschema
from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    SystemMessage,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage,
    query,
)
from claude_agent_sdk._version import __version__ as SDK_VERSION

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "template"
RESULTS = HERE / "results.jsonl"
MODEL = "claude-opus-5-5"

FINDINGS_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "file": {"type": "string"},
                    "line": {"type": "integer"},
                    "problem": {"type": "string"},
                    "case": {"type": "string"},
                },
                "required": ["id", "file", "line", "problem", "case"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["findings"],
    "additionalProperties": False,
}

TOLD_PROMPT = (
    "You are the quality reviewer for a change in this repo. The change is the set of changes "
    "not yet committed. Run Claude Code's stock code review on them, with no target, so it "
    "reviews the changes not yet committed. Then hand back every finding it reports in your "
    "result schema: an ID such as F1, the file and line, the problem, and a concrete case "
    "where it goes wrong. Don't change any file."
)

PROMPTS = {"init": "Reply with the single word: ok", "slash": "/code-review", "told": TOLD_PROMPT}


def fresh_copy(case: str) -> Path:
    dest = HERE / "runs" / f"{case}-{int(time.time())}"
    shutil.copytree(TEMPLATE, dest)
    return dest


async def run(case: str) -> dict:
    cwd = fresh_copy(case)
    options = ClaudeAgentOptions(
        model=MODEL,
        cwd=str(cwd),
        setting_sources=["project"],
        permission_mode="bypassPermissions",
        disallowed_tools=[
            "Edit",
            "Write",
            "NotebookEdit",
            "Bash(gh:*)",
            "Bash(git push:*)",
            "Bash(git commit:*)",
        ],
        max_turns=1 if case == "init" else 100,
        output_format=None
        if case == "init"
        else {"type": "json_schema", "schema": FINDINGS_SCHEMA},
    )
    record: dict = {"case": case, "sdk": SDK_VERSION, "model": MODEL, "cwd": str(cwd)}
    tool_uses: list[dict] = []
    texts: list[str] = []
    async for msg in query(prompt=PROMPTS[case], options=options):
        if isinstance(msg, SystemMessage) and msg.subtype == "init":
            d = msg.data
            record["cli_version"] = d.get("claude_code_version")
            record["skills"] = d.get("skills")
            record["slash_commands"] = d.get("slash_commands")
            record["tools"] = d.get("tools")
        elif isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, ToolUseBlock):
                    tool_uses.append({"name": block.name, "input": block.input})
                elif hasattr(block, "text"):
                    texts.append(block.text)
        elif isinstance(msg, UserMessage) and isinstance(msg.content, list):
            for block in msg.content:
                if isinstance(block, ToolResultBlock):
                    c = block.content
                    text = c if isinstance(c, str) else json.dumps(c)
                    record.setdefault("tool_results", []).append(text[:1500])
        elif isinstance(msg, ResultMessage):
            record["subtype"] = msg.subtype
            record["is_error"] = msg.is_error
            record["num_turns"] = msg.num_turns
            record["cost_usd"] = msg.total_cost_usd
            record["structured_output"] = msg.structured_output
            record["result_text"] = msg.result
    record["tool_uses"] = tool_uses
    record["texts"] = texts
    so = record.get("structured_output")
    if so is not None:
        try:
            jsonschema.validate(so, FINDINGS_SCHEMA)
            record["schema_ok"] = True
        except jsonschema.ValidationError as e:
            record["schema_ok"] = f"invalid: {e.message}"
    with RESULTS.open("a") as f:
        f.write(json.dumps(record) + "\n")
    return record


if __name__ == "__main__":
    rec = asyncio.run(run(sys.argv[1]))
    print(json.dumps(rec, indent=2)[:20000])
