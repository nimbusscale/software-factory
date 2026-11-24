"""Check the quality reviewer's prompt against the stock code review's prompt at high.

Usage: env -u CLAUDECODE .venv/bin/python run.py <case>...   (case: pr30-stock, pr30-ours, ...)
Each case reviews its clone under clones/, and writes runs/<case>.json.
"""

import asyncio
import json
import re
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
SF = Path("/home/jjk3/PycharmProjects/personal/software-factory-issue-82")
MODEL = "claude-opus-5-5"
RANGES = {
    "pr30": "2682d24..d1107ab",
    "pr32": "96305ff..2be1432",
    "pr33": "66a8031..4b99253",
    "pr35": "520127f..94e8306",
}


def stock_prompt(target: str) -> str:
    text = (SF / "docs/research/code-review-spike/stock-prompt-high-2.1.331.md").read_text()
    body = text.split("\n---\n", 1)[1].lstrip("\n")
    return f"Review target: `{target}`\n\n{body}"


def our_prompt(target: str) -> str:
    text = (SF / "src/software_factory/prompts/quality-reviewer.md").read_text()
    return text.replace("{{review_target}}", f"`{target}`")


def parse_findings(text: str | None):
    if not text:
        return None
    blocks = re.findall(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.S)
    candidates = blocks[::-1] or [text[text.find("[") : text.rfind("]") + 1]]
    for c in candidates:
        try:
            return json.loads(c)
        except json.JSONDecodeError:
            continue
    return None


async def run(case: str) -> None:
    pr, which = case.split("-")
    target = RANGES[pr]
    prompt = stock_prompt(target) if which == "stock" else our_prompt(target)
    cwd = HERE / "clones" / case
    options = ClaudeAgentOptions(
        model=MODEL,
        cwd=str(cwd),
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
    record["seconds"] = round(time.time() - start)
    record["tool_uses"] = tool_uses
    record["findings"] = parse_findings(record.get("result_text"))
    out = HERE / "runs" / f"{case}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(record, indent=2))
    n = len(record["findings"]) if record["findings"] is not None else "unparsed"
    print(f"{case}: {record.get('subtype')} findings={n} cost=${record.get('cost_usd')} {record['seconds']}s", flush=True)


async def main(cases: list[str]) -> None:
    await asyncio.gather(*(run(c) for c in cases))


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
