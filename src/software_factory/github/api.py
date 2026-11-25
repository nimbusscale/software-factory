import asyncio
import json
import os
import shutil
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from pydantic import BaseModel, ConfigDict, JsonValue, ValidationError
from pydantic.alias_generators import to_camel

if TYPE_CHECKING:
    from collections.abc import Mapping


class GitHubError(Exception):
    """A request to GitHub failed, or its reply doesn't fit its schema (TR-15).

    The message says why, in words for the owner.
    """


class GraphQL(Protocol):
    """Sends one request to GitHub's GraphQL API, and hands back the reply's JSON.

    `gh_graphql`, or a fake GitHub in tests.
    """

    async def __call__(
        self, query: str, variables: Mapping[str, JsonValue], /
    ) -> JsonValue: ...


class Reply(BaseModel):
    """The schema for the data in a reply from GitHub (TR-14, TD-10).

    Strict, so a field of the wrong type doesn't fit, such as a number given as text.
    Each field is read from the camelCase name GitHub gives it, such as `commentEdge`
    for `comment_edge`.
    """

    model_config = ConfigDict(strict=True, frozen=True, alias_generator=to_camel)


@dataclass(frozen=True)
class Repo:
    owner: str
    name: str

    @classmethod
    def parse(cls, owner_and_name: str) -> Repo:
        """Reads a repo given as `owner/name`, such as `nimbusscale/dust-law`."""
        owner, slash, name = owner_and_name.partition("/")
        if not owner or not slash or not name or "/" in name:
            message = f"{owner_and_name!r} isn't a repo. Give it as owner/name."
            raise ValueError(message)
        return cls(owner=owner, name=name)

    def __str__(self) -> str:
        return f"{self.owner}/{self.name}"


async def ask[ReplyT: Reply](
    graphql: GraphQL,
    query: str,
    variables: Mapping[str, JsonValue],
    reply_model: type[ReplyT],
) -> ReplyT:
    """Sends the request, and checks the reply's data against `reply_model`."""
    reply = await graphql(query, variables)
    data = reply.get("data") if isinstance(reply, dict) else None
    try:
        return reply_model.model_validate(data)
    except ValidationError as error:
        message = f"A reply from GitHub doesn't fit its schema: {error}"
        raise GitHubError(message) from error


async def gh_graphql(query: str, variables: Mapping[str, JsonValue]) -> JsonValue:
    """Sends the request with the GitHub CLI, logged in as the machine's user."""
    executable = shutil.which("gh")
    if executable is None:
        message = "The GitHub CLI, gh, isn't installed, or isn't on the PATH."
        raise GitHubError(message)
    # A run has no one at the terminal, so gh fails rather than ask a question.
    env = {**os.environ, "GH_PROMPT_DISABLED": "1"}
    process = await asyncio.create_subprocess_exec(
        *(executable, "api", "graphql", "--input", "-"),
        env=env,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    request = json.dumps({"query": query, "variables": dict(variables)})
    stdout, stderr = await process.communicate(request.encode())
    if process.returncode != 0:
        message = f"A request to GitHub failed: {stderr.decode().strip()}"
        raise GitHubError(message)
    try:
        reply: JsonValue = json.loads(stdout)
    except json.JSONDecodeError as error:
        message = f"A reply from GitHub isn't JSON: {error}"
        raise GitHubError(message) from error
    return reply
