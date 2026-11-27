from enum import Enum, auto
from typing import TYPE_CHECKING

from software_factory.config import StatusKey, factory_config
from software_factory.github.api import GitHubError, GraphQL, Reply, ask
from software_factory.github.issue import Issue, post_comment

if TYPE_CHECKING:
    from collections.abc import Mapping

    from pydantic import JsonValue

READ_BOARD = """
query ReadBoard($owner: String!, $number: Int!) {
  repositoryOwner(login: $owner) {
    ... on ProjectV2Owner {
      projectV2(number: $number) {
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


class BoardOwner(Reply):
    project_v2: Board


class ReadBoardReply(Reply):
    repository_owner: BoardOwner


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


async def read_board(graphql: GraphQL) -> tuple[Board, StatusField]:
    """The board the factory's config names.

    Every project the factory runs on shares the one board, so a run goes straight to
    it, and doesn't look for it through the repo's links. A repo can link to any number
    of boards.
    """
    name = factory_config().board
    variables: dict[str, JsonValue] = {"owner": name.owner, "number": name.number}
    reply = await ask(graphql, READ_BOARD, variables, ReadBoardReply)
    board = reply.repository_owner.project_v2
    if board.field is None:
        message = f"The board {board.title!r} has no Status field."
        raise GitHubError(message)
    return board, board.field


async def move_issue(graphql: GraphQL, issue: Issue, moment: Moment) -> None:
    """Moves the issue to the status the board shows at `moment`.

    Adds the issue to the board first, when it isn't on it.
    """
    board, field = await read_board(graphql)
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


async def end_without_pr(graphql: GraphQL, issue: Issue, reason: str) -> None:
    """Meets FR-14 and FR-13. `reason` says why the run ended, for the owner."""
    body = f"The factory's run on this issue ended without a PR.\n\n{reason}"
    await post_comment(graphql, issue.id, body)
    await move_issue(graphql, issue, Moment.RUN_ENDED_WITHOUT_PR)
