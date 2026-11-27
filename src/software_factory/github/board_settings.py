"""Reads what the board setup compares with the board file and the factory's config."""

from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal

from software_factory.github.api import GraphQL, Reply, ask

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from pydantic import JsonValue

type ViewLayout = Literal["BOARD_LAYOUT", "TABLE_LAYOUT", "ROADMAP_LAYOUT"]

READ_OWNER_BOARDS = """
query ReadOwnerBoards($owner: String!) {
  repositoryOwner(login: $owner) {
    id
    ... on ProjectV2Owner {
      projectsV2(first: 100) { nodes { number title closed } }
    }
  }
}
"""

READ_BOARD_SETTINGS = """
query ReadBoardSettings($owner: String!, $number: Int!) {
  repositoryOwner(login: $owner) {
    ... on ProjectV2Owner {
      projectV2(number: $number) {
        id
        fields(first: 100) { nodes { ... on ProjectV2FieldCommon { id name } } }
        views(first: 100) {
          nodes {
            id name layout filter
            fields(first: 100) { nodes { ... on ProjectV2FieldCommon { name } } }
          }
        }
        workflows(first: 100) { nodes { id name } }
        repositories(first: 100) {
          nodes {
            id nameWithOwner
            labels(first: 100) { nodes { id name color description } }
          }
        }
      }
    }
  }
}
"""


class SetUpError(Exception):
    """The board can't be set up. The message says why, in words for the owner."""


@dataclass(frozen=True)
class Change:
    """One way GitHub differs from the board file or the config, and its fix."""

    # What differs, a line each.
    lines: tuple[str, ...]
    apply: Callable[[], Awaitable[None]]


class OwnerBoard(Reply):
    number: int
    title: str
    closed: bool


class OwnerBoards(Reply):
    nodes: list[OwnerBoard]


class Owner(Reply):
    id: str
    projects_v2: OwnerBoards


class ReadOwnerBoardsReply(Reply):
    repository_owner: Owner


class FieldName(Reply):
    name: str


class BoardField(Reply):
    id: str
    name: str


class BoardFields(Reply):
    nodes: list[BoardField]


class VisibleFields(Reply):
    nodes: list[FieldName]


class BoardView(Reply):
    id: str
    name: str
    layout: ViewLayout
    # GitHub gives a view with no filter as null or as "".
    filter: str | None
    fields: VisibleFields


class BoardViews(Reply):
    nodes: list[BoardView]


class Workflow(Reply):
    id: str
    name: str


class Workflows(Reply):
    nodes: list[Workflow]


class Label(Reply):
    id: str
    name: str
    color: str
    description: str | None


class Labels(Reply):
    nodes: list[Label]


class LinkedRepo(Reply):
    id: str
    name_with_owner: str
    labels: Labels


class LinkedRepos(Reply):
    nodes: list[LinkedRepo]


class BoardSettings(Reply):
    id: str
    fields: BoardFields
    views: BoardViews
    workflows: Workflows
    repositories: LinkedRepos


class SettingsOwner(Reply):
    project_v2: BoardSettings


class ReadBoardSettingsReply(Reply):
    repository_owner: SettingsOwner


async def read_owner(graphql: GraphQL, owner: str) -> Owner:
    variables: dict[str, JsonValue] = {"owner": owner}
    reply = await ask(graphql, READ_OWNER_BOARDS, variables, ReadOwnerBoardsReply)
    return reply.repository_owner


async def read_board_settings(
    graphql: GraphQL, owner: str, number: int
) -> BoardSettings:
    variables: dict[str, JsonValue] = {"owner": owner, "number": number}
    reply = await ask(graphql, READ_BOARD_SETTINGS, variables, ReadBoardSettingsReply)
    return reply.repository_owner.project_v2
