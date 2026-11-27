"""Makes the factory's board match the board file and the factory's config.

Run it from the repo root with `uv run set-up-board`. With `--check`, it lists how
GitHub differs and changes nothing.
"""

import argparse
import asyncio
import sys
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import ValidationError

from software_factory.config import factory_config
from software_factory.github.api import GitHubError, GraphQL, Reply, ask, gh_graphql
from software_factory.github.board import StatusField, read_board
from software_factory.github.board_settings import (
    BoardSettings,
    Change,
    OwnerBoard,
    SetUpError,
    read_board_settings,
    read_owner,
)
from software_factory.github.board_views import BoardFile, view_changes
from software_factory.github.repo_labels import label_changes

if TYPE_CHECKING:
    from pydantic import JsonValue

BOARD_FILE = Path("board/board.toml")

# It moves an issue to In review when a PR links the issue. A run's PR links its issue,
# so after the run moves the issue to Needs attention, it could move it back (FR-29).
# GitHub's API can delete a built-in workflow, but can't turn one off.
LINKED_PULL_REQUEST_WORKFLOW = "Pull request linked to issue"

CREATE_BOARD = """
mutation CreateBoard($ownerId: ID!, $title: String!) {
  createProjectV2(input: {ownerId: $ownerId, title: $title}) {
    projectV2 { number }
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

DELETE_WORKFLOW = """
mutation DeleteWorkflow($workflowId: ID!) {
  deleteProjectV2Workflow(input: {workflowId: $workflowId}) { deletedWorkflowId }
}
"""


class BoardNumber(Reply):
    number: int


class CreatedBoard(Reply):
    project_v2: BoardNumber


class CreateBoardReply(Reply):
    create_project_v2: CreatedBoard


class FieldId(Reply):
    id: str


class UpdatedField(Reply):
    project_v2_field: FieldId


class SetStatusOptionsReply(Reply):
    update_project_v2_field: UpdatedField


class DeletedWorkflow(Reply):
    deleted_workflow_id: str


class DeleteWorkflowReply(Reply):
    delete_project_v2_workflow: DeletedWorkflow


async def set_up_board(
    graphql: GraphQL, board_file: BoardFile, *, check: bool
) -> list[str]:
    """Hands back a line for each way GitHub differed. Changes nothing when `check`."""
    name = factory_config().board
    owner = await read_owner(graphql, name.owner)
    found = next((b for b in owner.projects_v2.nodes if b.number == name.number), None)
    lines: list[str] = []
    if found is None:
        lines.append(
            f"{name.owner} has no board #{name.number}."
            f" A board titled {board_file.title!r} gets created."
        )
        if check:
            return lines
        number = await create_board(graphql, owner.id, board_file.title)
        if number != name.number:
            message = (
                f"{lines[0]} It's #{number}. Set board.number to {number} in the"
                " factory's config, then run this again."
            )
            raise SetUpError(message)
    else:
        check_it_is_the_board(found, board_file)
    _, field = await read_board(graphql)
    settings = await read_board_settings(graphql, name.owner, name.number)
    for change in board_changes(graphql, field, settings, board_file):
        if not check:
            await change.apply()
        lines.extend(change.lines)
    return lines


def check_it_is_the_board(board: OwnerBoard, board_file: BoardFile) -> None:
    """Refuses a board the config names by mistake, so its settings stay as they are."""
    if board.title != board_file.title:
        message = (
            f"The board #{board.number} is titled {board.title!r}, and the board file"
            f" says {board_file.title!r}. Check board.number in the factory's config."
        )
        raise SetUpError(message)
    if board.closed:
        message = f"The board #{board.number} is closed. Reopen it on GitHub."
        raise SetUpError(message)


async def create_board(graphql: GraphQL, owner_id: str, title: str) -> int:
    variables: dict[str, JsonValue] = {"ownerId": owner_id, "title": title}
    reply = await ask(graphql, CREATE_BOARD, variables, CreateBoardReply)
    return reply.create_project_v2.project_v2.number


def board_changes(
    graphql: GraphQL, field: StatusField, settings: BoardSettings, board_file: BoardFile
) -> list[Change]:
    changes = [
        *status_changes(graphql, field),
        *view_changes(graphql, settings, board_file),
        *workflow_changes(graphql, settings),
    ]
    for repo in settings.repositories.nodes:
        changes.extend(label_changes(graphql, repo))
    return changes


def status_changes(graphql: GraphQL, field: StatusField) -> list[Change]:
    statuses = list(factory_config().statuses.values())
    # A status whose name differs only in case is renamed, not removed and added, so the
    # issues in it keep their status.
    by_name = {option.name.casefold(): option for option in field.options}
    lines: list[str] = []
    for status in statuses:
        option = by_name.get(status.name.casefold())
        if option is None:
            lines.append(f"The board has no status {status.name!r}. It gets added.")
        elif (option.name, option.color, option.description) != (
            status.name,
            status.color,
            status.description,
        ):
            lines.append(
                f"The status {option.name!r} has a different name, color or"
                f" description from {status.name!r}."
            )
    wanted = [status.name for status in statuses]
    wanted_names = {name.casefold() for name in wanted}
    lines.extend(
        f"The status {option.name!r} isn't in the factory's config. It gets removed,"
        " which takes it off every issue in it."
        for option in field.options
        if option.name.casefold() not in wanted_names
    )
    if not lines and [option.name for option in field.options] != wanted:
        lines.append("The board's statuses are in a different order from the config's.")
    if not lines:
        return []
    # GitHub replaces every option with the ones given. Each one keeps its ID, or GitHub
    # clears the status of every issue in it.
    options: list[JsonValue] = [
        {
            **(
                {"id": by_name[status.name.casefold()].id}
                if status.name.casefold() in by_name
                else {}
            ),
            "name": status.name,
            "color": status.color,
            "description": status.description,
        }
        for status in statuses
    ]

    async def apply() -> None:
        variables: dict[str, JsonValue] = {"fieldId": field.id, "options": options}
        await ask(graphql, SET_STATUS_OPTIONS, variables, SetStatusOptionsReply)

    return [Change(tuple(lines), apply)]


def workflow_changes(graphql: GraphQL, settings: BoardSettings) -> list[Change]:
    changes: list[Change] = []
    for workflow in settings.workflows.nodes:
        if workflow.name != LINKED_PULL_REQUEST_WORKFLOW:
            continue
        line = (
            f"The board has the built-in workflow {workflow.name!r}. It gets deleted."
        )

        async def apply(workflow_id: str = workflow.id) -> None:
            variables: dict[str, JsonValue] = {"workflowId": workflow_id}
            await ask(graphql, DELETE_WORKFLOW, variables, DeleteWorkflowReply)

        changes.append(Change((line,), apply))
    return changes


def read_board_file(path: Path) -> BoardFile:
    try:
        return BoardFile.model_validate(tomllib.loads(path.read_text(encoding="utf-8")))
    except FileNotFoundError as error:
        message = f"There's no board file at {path}. Run this from the repo's root."
        raise SetUpError(message) from error
    except (tomllib.TOMLDecodeError, ValidationError) as error:
        message = f"The board file {path} isn't valid: {error}"
        raise SetUpError(message) from error


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Makes the factory's board match the board file and the config."
    )
    parser.add_argument(
        "--check", action="store_true", help="list how GitHub differs, change nothing"
    )
    check: bool = parser.parse_args().check
    try:
        board_file = read_board_file(BOARD_FILE)
        lines = asyncio.run(set_up_board(gh_graphql, board_file, check=check))
    except (SetUpError, GitHubError) as error:
        sys.exit(str(error))
    sys.stdout.writelines(f"{line}\n" for line in lines)
    if not lines:
        sys.stdout.write("The board matches the board file and the config.\n")
    elif check:
        sys.exit(1)
