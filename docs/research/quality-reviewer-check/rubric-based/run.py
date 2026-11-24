"""Review four road-trip-agent changes with the quality reviewer's prompt and rubric.

Usage: env -u CLAUDECODE <venv>/bin/python run.py <prompt file> <case>...   (case: pr30, pr32, ...)
Each case reviews its clone under clones/, which holds the rubric at docs/standards/review-rubric.md,
and writes runs/<case>.json.
"""

import asyncio
import json
import sys
import time
from pathlib import Path

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    SystemMessage,
    ToolUseBlock,
    query,
)
from claude_agent_sdk._version import __version__ as SDK_VERSION

HERE = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"
RANGES = {
    "pr30": "2682d24..d1107ab",
    "pr32": "96305ff..2be1432",
    "pr33": "66a8031..4b99253",
    "pr35": "520127f..94e8306",
}

PLACE = {"file": {"type": "string"}, "line": {"type": "integer"}}
FINDING = {
    "type": "object",
    "additionalProperties": False,
    "required": ["id", "file", "line", "label", "mark", "problem", "failure_case", "label_reason"],
    "properties": {
        "id": {"type": "string"},
        **PLACE,
        "label": {"type": "string"},
        "mark": {"enum": ["important", "pre_existing", "nit", "to_check"]},
        "problem": {"type": "string"},
        "failure_case": {"type": "string"},
        "label_reason": {"type": "string"},
    },
}
DROPPED = {
    "type": "object",
    "additionalProperties": False,
    "required": ["file", "line", "problem", "label", "reason"],
    "properties": {
        **PLACE,
        "problem": {"type": "string"},
        "label": {"type": "string"},
        "reason": {"type": "string"},
    },
}
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["status", "reason", "findings", "dropped"],
    "properties": {
        "status": {"enum": ["done", "stopped"]},
        "reason": {"type": "string"},
        "findings": {"type": "array", "items": FINDING},
        "dropped": {"type": "array", "items": DROPPED},
    },
}


async def run(prompt_file: Path, case: str) -> None:
    target = RANGES[case]
    prompt = prompt_file.read_text().replace("{{review_target}}", f"`{target}`")
    options = ClaudeAgentOptions(
        model=MODEL,
        cwd=str(HERE / "clones" / case),
        setting_sources=["project"],
        permission_mode="bypassPermissions",
        disallowed_tools=[
            "Edit",
            "Write",
            "NotebookEdit",
            "Agent",
            "Task",
            "WebFetch",
            "WebSearch",
            "Bash(gh:*)",
            "Bash(ssh:*)",
            "Bash(curl:*)",
            "Bash(wget:*)",
            "Bash(git push:*)",
            "Bash(git commit:*)",
            "Bash(git fetch:*)",
            "Bash(git pull:*)",
        ],
        max_turns=200,
        output_format={"type": "json_schema", "schema": SCHEMA},
    )
    record: dict = {"case": case, "target": target, "sdk": SDK_VERSION, "model": MODEL}
    tool_uses: list[dict] = []
    start = time.time()
    async for msg in query(prompt=prompt, options=options):
        if isinstance(msg, SystemMessage) and msg.subtype == "init":
            record["cli_version"] = msg.data.get("claude_code_version")
        elif isinstance(msg, AssistantMessage):
            for block in msg.content:
                if isinstance(block, ToolUseBlock):
                    tool_uses.append({"name": block.name, "input": block.input})
        elif isinstance(msg, ResultMessage):
            record["subtype"] = msg.subtype
            record["is_error"] = msg.is_error
            record["num_turns"] = msg.num_turns
            record["cost_usd"] = msg.total_cost_usd
            record["usage"] = msg.usage
            record["result_text"] = msg.result
            record["result"] = msg.structured_output
    record["seconds"] = round(time.time() - start)
    record["tool_uses"] = tool_uses
    out = HERE / "runs" / f"{case}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(record, indent=2))
    res = record.get("result") or {}
    print(
        f"{case}: {record.get('subtype')} findings={len(res.get('findings', []))} "
        f"dropped={len(res.get('dropped', []))} cost=${record.get('cost_usd')} {record['seconds']}s",
        flush=True,
    )


async def main(prompt_file: str, cases: list[str]) -> None:
    await asyncio.gather(*(run(Path(prompt_file), c) for c in cases))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1], sys.argv[2:]))
