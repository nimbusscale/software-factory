"""A fake Agent SDK for tests: the real `query`, over a transport that replays messages.

The SDK's own code then parses each message and handles errors, as it does with Claude
Code.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import anyio
from claude_agent_sdk import ClaudeAgentOptions, Message, ProcessError, Transport, query

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from pydantic import JsonValue

SAVED_RESPONSES = Path(__file__).parent / "saved_responses"

type RawMessage = dict[str, JsonValue]


def saved_response(name: str) -> list[RawMessage]:
    """The messages in a saved response from Claude Code, one JSON object a line."""
    text = (SAVED_RESPONSES / f"{name}.jsonl").read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines()]


def result_message(**fields: JsonValue) -> RawMessage:
    """A result message, with the fields Claude Code always sends, and `fields`."""
    message: RawMessage = {
        "type": "result",
        "subtype": "success",
        "is_error": False,
        "duration_ms": 1000,
        "duration_api_ms": 900,
        "num_turns": 2,
        "session_id": "11111111-2222-3333-4444-555555555555",
        "result": "",
    }
    message.update(fields)
    return message


class ReplayTransport(Transport):
    def __init__(self, messages: list[RawMessage]) -> None:
        self._messages = messages
        self._send, self._receive = anyio.create_memory_object_stream[RawMessage](100)

    async def connect(self) -> None:
        pass

    async def write(self, data: str) -> None:
        request = json.loads(data)
        if request.get("type") == "control_request":
            response: RawMessage = {
                "type": "control_response",
                "response": {
                    "subtype": "success",
                    "request_id": request["request_id"],
                    "response": {},
                },
            }
            await self._send.send(response)
        elif request.get("type") == "user":
            for message in self._messages:
                await self._send.send(message)
            await self._send.aclose()

    async def read_messages(self) -> AsyncIterator[RawMessage]:
        async for message in self._receive:
            yield message
        last = self._messages[-1] if self._messages else {}
        if last.get("is_error") is True:
            # Claude Code exits with 1 after an error result.
            error = "Command failed with exit code 1"
            raise ProcessError(error, exit_code=1)

    async def close(self) -> None:
        await self._send.aclose()

    def is_ready(self) -> bool:
        return True

    async def end_input(self) -> None:
        pass


@dataclass
class FakeQuery:
    """Replays one list of messages for each call, and keeps each call's options."""

    responses: list[list[RawMessage]]
    options: list[ClaudeAgentOptions] = field(default_factory=list)

    def __call__(
        self, *, prompt: str, options: ClaudeAgentOptions
    ) -> AsyncIterator[Message]:
        self.options.append(options)
        transport = ReplayTransport(self.responses.pop(0))
        return query(prompt=prompt, options=options, transport=transport)
