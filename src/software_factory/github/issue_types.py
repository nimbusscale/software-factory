"""The changes that give the board's owner the factory's issue types."""

from typing import TYPE_CHECKING

from software_factory.config import IssueType, factory_config
from software_factory.github.api import GraphQL, Reply, ask
from software_factory.github.board_settings import (
    Change,
    Owner,
    OwnerIssueType,
    SetUpError,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from pydantic import JsonValue

CREATE_ISSUE_TYPE = """
mutation CreateIssueType(
  $ownerId: ID!, $name: String!, $color: IssueTypeColor!, $description: String!
) {
  createIssueType(input: {
    ownerId: $ownerId, name: $name, color: $color, description: $description,
    isEnabled: true
  }) {
    issueType { id }
  }
}
"""

UPDATE_ISSUE_TYPE = """
mutation UpdateIssueType(
  $id: ID!, $name: String!, $color: IssueTypeColor!, $description: String!
) {
  updateIssueType(input: {
    issueTypeId: $id, name: $name, color: $color, description: $description,
    isEnabled: true
  }) {
    issueType { id }
  }
}
"""

DELETE_ISSUE_TYPE = """
mutation DeleteIssueType($id: ID!) {
  deleteIssueType(input: {issueTypeId: $id}) { deletedIssueTypeId }
}
"""


class IssueTypeId(Reply):
    id: str


class ChangedIssueType(Reply):
    issue_type: IssueTypeId


class CreateIssueTypeReply(Reply):
    create_issue_type: ChangedIssueType


class UpdateIssueTypeReply(Reply):
    update_issue_type: ChangedIssueType


class DeletedIssueType(Reply):
    deleted_issue_type_id: str


class DeleteIssueTypeReply(Reply):
    delete_issue_type: DeletedIssueType


def issue_type_changes(graphql: GraphQL, name: str, owner: Owner) -> list[Change]:
    if owner.issue_types is None:
        message = (
            f"{name} isn't an organization, so it can't have the factory's issue types."
            " The board's owner has to be an organization."
        )
        raise SetUpError(message)
    wanted = factory_config().issue_types
    # A type whose name differs only in case is renamed, not deleted and created, so
    # the issues that have it keep it.
    by_name = {found.name.casefold(): found for found in owner.issue_types.nodes}
    changes: list[Change] = []
    for type_name, issue_type in wanted.items():
        found = by_name.get(type_name.casefold())
        if found is None:
            lines = (f"{name} has no issue type {type_name!r}. It gets created.",)
            apply = create_issue_type(graphql, owner.id, type_name, issue_type)
            changes.append(Change(lines, apply))
        elif (found.name, found.color, found.description or "", found.is_enabled) != (
            type_name,
            issue_type.color,
            issue_type.description,
            True,
        ):
            line = (
                f"{name}'s issue type {found.name!r} has a different name, color,"
                f" description or setting from {type_name!r}."
            )
            apply = update_issue_type(graphql, found.id, type_name, issue_type)
            changes.append(Change((line,), apply))
    wanted_names = {type_name.casefold() for type_name in wanted}
    for found in owner.issue_types.nodes:
        if found.name.casefold() not in wanted_names:
            line = (
                f"{name}'s issue type {found.name!r} isn't in the factory's config. It"
                " gets deleted, which takes it off every issue that has it."
            )
            changes.append(Change((line,), delete_issue_type(graphql, found)))
    return changes


def create_issue_type(
    graphql: GraphQL, owner_id: str, name: str, issue_type: IssueType
) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        variables: dict[str, JsonValue] = {
            "ownerId": owner_id,
            "name": name,
            "color": issue_type.color,
            "description": issue_type.description,
        }
        await ask(graphql, CREATE_ISSUE_TYPE, variables, CreateIssueTypeReply)

    return apply


def update_issue_type(
    graphql: GraphQL, type_id: str, name: str, issue_type: IssueType
) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        variables: dict[str, JsonValue] = {
            "id": type_id,
            "name": name,
            "color": issue_type.color,
            "description": issue_type.description,
        }
        await ask(graphql, UPDATE_ISSUE_TYPE, variables, UpdateIssueTypeReply)

    return apply


def delete_issue_type(
    graphql: GraphQL, issue_type: OwnerIssueType
) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        variables: dict[str, JsonValue] = {"id": issue_type.id}
        await ask(graphql, DELETE_ISSUE_TYPE, variables, DeleteIssueTypeReply)

    return apply
