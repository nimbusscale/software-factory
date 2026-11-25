import argparse
import asyncio
from enum import Enum, auto
from typing import TYPE_CHECKING

from software_factory.config import BoardStatus, StatusKey, factory_config
from software_factory.github.api import (
    GitHubError,
    GraphQL,
    Reply,
    Repo,
    ask,
    gh_graphql,
)
from software_factory.github.issue import Issue, post_comment

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping

    from pydantic import JsonValue

READ_BOARD = """
query ReadBoard($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    projectsV2(first: 1) {
      totalCount
      nodes {
        id
        title
        field(name: "Status") {
          ... on ProjectV2SingleSelectField { id options { id name color description } }
        }
      }
    }
  }
}
"""

ADD_ITEM = """
mutation AddItem($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
    item { id }
  }
}
"""

SET_ITEM_STATUS = """
mutation SetItemStatus(
  $projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!
) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $projectId, itemId: $itemId, fieldId: $fieldId,
    value: {singleSelectOptionId: $optionId}
  }) {
    projectV2Item { id }
  }
}
"""

SET_STATUS_OPTIONS = """
mutation SetStatusOptions(
  $fieldId: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]!
) {
  updateProjectV2Field(input: {fieldId: $fieldId, singleSelectOptions: $options}) {
    projectV2Field { ... on ProjectV2SingleSelectField { id } }
  }
}
"""


class Moment(Enum):
    RUN_STARTED = auto()
    PR_OPENED = auto()
    PR_OPENED_WITH_FINDING_TO_CHECK = auto()
    RUN_ENDED_WITHOUT_PR = auto()


STATUS_AT: Mapping[Moment, StatusKey] = {
    Moment.RUN_STARTED: "in_development",  # FR-11
    Moment.PR_OPENED: "in_review",  # FR-28
    Moment.PR_OPENED_WITH_FINDING_TO_CHECK: "needs_attention",  # FR-29
    Moment.RUN_ENDED_WITHOUT_PR: "needs_attention",  # FR-13
}


class StatusOption(Reply):
    id: str
    name: str
    color: str
    description: str


class StatusField(Reply):
    id: str
    options: list[StatusOption]


class Board(Reply):
    id: str
    title: str
    # None when the board has no field named Status.
    field: StatusField | None


class Boards(Reply):
    total_count: int
    nodes: list[Board]


class BoardRepository(Reply):
    projects_v2: Boards


class ReadBoardReply(Reply):
    repository: BoardRepository


class Item(Reply):
    id: str


class AddedItem(Reply):
    item: Item


class AddItemReply(Reply):
    add_project_v2_item_by_id: AddedItem


class UpdatedItem(Reply):
    project_v2_item: Item


class SetItemStatusReply(Reply):
    update_project_v2_item_field_value: UpdatedItem


class UpdatedField(Reply):
    project_v2_field: Item


class SetStatusOptionsReply(Reply):
    update_project_v2_field: UpdatedField


async def read_board(graphql: GraphQL, repo: Repo) -> tuple[Board, StatusField]:
    """The project's board: the one GitHub project linked to its repo."""
    variables: dict[str, JsonValue] = {"owner": repo.owner, "name": repo.name}
    reply = await ask(graphql, READ_BOARD, variables, ReadBoardReply)
    boards = reply.repository.projects_v2
    if boards.total_count != 1:
        message = (
            f"The repo {repo} has {boards.total_count} GitHub projects linked to it,"
            " and the factory needs exactly one, as the project's board."
        )
        raise GitHubError(message)
    if not boards.nodes:
        message = (
            f"GitHub lists a project linked to the repo {repo}, but doesn't show it."
            " The GitHub CLI's login may not have access to it."
        )
        raise GitHubError(message)
    board = boards.nodes[0]
    if board.field is None:
        message = f"The board {board.title!r} has no Status field."
        raise GitHubError(message)
    return board, board.field


async def move_issue(
    graphql: GraphQL, repo: Repo, issue: Issue, moment: Moment
) -> None:
    """Moves the issue to the status the board shows at `moment`.

    Adds the issue to the board first, when it isn't on it.
    """
    board, field = await read_board(graphql, repo)
    status = factory_config().statuses[STATUS_AT[moment]]
    option = next((o for o in field.options if o.name == status.name), None)
    if option is None:
        message = (
            f"The board {board.title!r} has no status {status.name!r}. Set the board's"
            " statuses from the factory's config."
        )
        raise GitHubError(message)
    # GitHub hands back the issue's item when the issue is already on the board.
    added = await ask(
        graphql,
        ADD_ITEM,
        {"projectId": board.id, "contentId": issue.id},
        AddItemReply,
    )
    variables: dict[str, JsonValue] = {
        "projectId": board.id,
        "itemId": added.add_project_v2_item_by_id.item.id,
        "fieldId": field.id,
        "optionId": option.id,
    }
    await ask(graphql, SET_ITEM_STATUS, variables, SetItemStatusReply)


async def end_without_pr(
    graphql: GraphQL, repo: Repo, issue: Issue, reason: str
) -> None:
    """Meets FR-14 and FR-13. `reason` says why the run ended, for the owner."""
    body = f"The factory's run on this issue ended without a PR.\n\n{reason}"
    await post_comment(graphql, issue.id, body)
    await move_issue(graphql, repo, issue, Moment.RUN_ENDED_WITHOUT_PR)


async def set_board_statuses(graphql: GraphQL, repo: Repo) -> None:
    """Sets the board's statuses from the factory's config, and keeps its others."""
    _, field = await read_board(graphql, repo)
    statuses = factory_config().statuses.values()
    options = status_options(field.options, statuses)
    variables: dict[str, JsonValue] = {"fieldId": field.id, "options": options}
    await ask(graphql, SET_STATUS_OPTIONS, variables, SetStatusOptionsReply)


def status_options(
    board_options: list[StatusOption], statuses: Iterable[BoardStatus]
) -> list[JsonValue]:
    by_name = {status.name: status for status in statuses}
    options: list[JsonValue] = []
    for option in board_options:
        status = by_name.pop(option.name, None)
        # GitHub replaces every option with the ones given. Each one keeps its ID, or
        # GitHub clears the status of every issue in it.
        options.append(
            {
                "id": option.id,
                "name": option.name,
                "color": option.color if status is None else status.color,
                "description": (
                    option.description if status is None else status.description
                ),
            }
        )
    options.extend(
        {"name": s.name, "color": s.color, "description": s.description}
        for s in by_name.values()
    )
    return options


def main() -> None:
    """Run it with `uv run set-board-statuses <owner/name>`."""
    parser = argparse.ArgumentParser(
        description="Sets a project's board statuses from the factory's config."
    )
    parser.add_argument("repo", help="the project's repo, owner/name")
    text: str = parser.parse_args().repo
    try:
        repo = Repo.parse(text)
    except ValueError as error:
        parser.error(str(error))
    asyncio.run(set_board_statuses(gh_graphql, repo))
