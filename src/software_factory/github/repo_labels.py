"""The changes that make each repo linked to the board have the factory's labels."""

from typing import TYPE_CHECKING

from software_factory.config import RepoLabel, factory_config
from software_factory.github.api import GraphQL, Reply, ask
from software_factory.github.board_settings import Change, Label, LinkedRepo

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from pydantic import JsonValue

# The labels GitHub adds to each new repo. `documentation` is among them, and goes
# because a change to docs only is a task.
GITHUB_DEFAULT_LABELS = frozenset(
    {
        "accessibility",
        "bug",
        "documentation",
        "duplicate",
        "enhancement",
        "good first issue",
        "help wanted",
        "invalid",
        "question",
        "wontfix",
    }
)

CREATE_LABEL = """
mutation CreateLabel(
  $repositoryId: ID!, $name: String!, $color: String!, $description: String!
) {
  createLabel(input: {
    repositoryId: $repositoryId, name: $name, color: $color, description: $description
  }) {
    label { id }
  }
}
"""

UPDATE_LABEL = """
mutation UpdateLabel($id: ID!, $color: String!, $description: String!) {
  updateLabel(input: {id: $id, color: $color, description: $description}) {
    label { id }
  }
}
"""

DELETE_LABEL = """
mutation DeleteLabel($id: ID!) {
  deleteLabel(input: {id: $id}) { clientMutationId }
}
"""


class LabelId(Reply):
    id: str


class ChangedLabel(Reply):
    label: LabelId


class CreateLabelReply(Reply):
    create_label: ChangedLabel


class UpdateLabelReply(Reply):
    update_label: ChangedLabel


class DeletedLabel(Reply):
    client_mutation_id: str | None


class DeleteLabelReply(Reply):
    delete_label: DeletedLabel


def label_changes(graphql: GraphQL, repo: LinkedRepo) -> list[Change]:
    wanted = factory_config().labels
    by_name = {label.name: label for label in repo.labels.nodes}
    where = repo.name_with_owner
    changes: list[Change] = []
    for name, label in wanted.items():
        found = by_name.get(name)
        if found is None:
            lines = (f"{where} has no label {name!r}. It gets created.",)
            changes.append(Change(lines, create_label(graphql, repo.id, name, label)))
        elif (found.color, found.description or "") != (label.color, label.description):
            lines = (f"{where}'s label {name!r} has a different color or description.",)
            changes.append(Change(lines, update_label(graphql, found.id, label)))
    for found in repo.labels.nodes:
        if found.name in GITHUB_DEFAULT_LABELS and found.name not in wanted:
            line = (
                f"{where} has GitHub's default label {found.name!r}. It gets deleted,"
                " which takes it off every issue that has it."
            )
            changes.append(Change((line,), delete_label(graphql, found)))
    return changes


def create_label(
    graphql: GraphQL, repo_id: str, name: str, label: RepoLabel
) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        variables: dict[str, JsonValue] = {
            "repositoryId": repo_id,
            "name": name,
            "color": label.color,
            "description": label.description,
        }
        await ask(graphql, CREATE_LABEL, variables, CreateLabelReply)

    return apply


def update_label(
    graphql: GraphQL, label_id: str, label: RepoLabel
) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        variables: dict[str, JsonValue] = {
            "id": label_id,
            "color": label.color,
            "description": label.description,
        }
        await ask(graphql, UPDATE_LABEL, variables, UpdateLabelReply)

    return apply


def delete_label(graphql: GraphQL, label: Label) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        await ask(graphql, DELETE_LABEL, {"id": label.id}, DeleteLabelReply)

    return apply
