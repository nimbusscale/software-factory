"""The changes that make a board's views match the board file."""

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

from software_factory.github.api import GraphQL, Reply, ask
from software_factory.github.board_settings import (
    BoardSettings,
    BoardView,
    Change,
    SetUpError,
    ViewLayout,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from pydantic import JsonValue

CREATE_VIEW = """
mutation CreateView(
  $projectId: ID!, $name: String!, $layout: ProjectV2ViewLayout!, $fieldIds: [ID!]
) {
  createProjectV2View(input: {
    projectId: $projectId, name: $name, layout: $layout,
    configuration: {visibleFieldIds: $fieldIds}
  }) {
    projectV2View { id }
  }
}
"""

UPDATE_VIEW = """
mutation UpdateView(
  $viewId: ID!, $layout: ProjectV2ViewLayout!, $filter: String!, $fieldIds: [ID!]
) {
  updateProjectV2View(input: {
    viewId: $viewId, layout: $layout, filter: $filter,
    configuration: {visibleFieldIds: $fieldIds}
  }) {
    projectV2View { id }
  }
}
"""

DELETE_VIEW = """
mutation DeleteView($viewId: ID!) {
  deleteProjectV2View(input: {viewId: $viewId}) { projectV2View { id } }
}
"""


class FileModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class ViewInFile(FileModel):
    name: str
    layout: ViewLayout
    filter: str
    # The names of the visible fields.
    fields: list[str]


class BoardFile(FileModel):
    title: str
    views: list[ViewInFile]


class ViewId(Reply):
    id: str


class CreatedView(Reply):
    project_v2_view: ViewId


class CreateViewReply(Reply):
    create_project_v2_view: CreatedView


class UpdateViewReply(Reply):
    update_project_v2_view: CreatedView


class DeleteViewReply(Reply):
    delete_project_v2_view: CreatedView


def view_changes(
    graphql: GraphQL, board: BoardSettings, board_file: BoardFile
) -> list[Change]:
    """Creates or updates each view in the file, then deletes the board's others.

    The deletes come last, since a board always keeps at least one view.
    """
    field_ids = {f.name: f.id for f in board.fields.nodes}
    views = board.views.nodes
    by_name = {view.name: view for view in views}
    changes: list[Change] = []
    for wanted in board_file.views:
        ids = visible_field_ids(wanted, field_ids)
        view = by_name.get(wanted.name)
        if view is None:
            changes.append(create_view(graphql, board.id, wanted, ids))
            continue
        lines = view_differences(view, wanted)
        if lines:
            changes.append(Change(lines, update_view(graphql, view.id, wanted, ids)))
    wanted_names = {view.name for view in board_file.views}
    changes.extend(
        Change(
            (f"The view {view.name!r} isn't in the board file. It gets deleted.",),
            delete_view(graphql, view.id),
        )
        for view in views
        if view.name not in wanted_names
    )
    return changes


def visible_field_ids(wanted: ViewInFile, field_ids: dict[str, str]) -> list[str]:
    missing = [name for name in wanted.fields if name not in field_ids]
    if missing:
        names = ", ".join(repr(name) for name in missing)
        message = (
            f"The view {wanted.name!r} names fields the board doesn't have: {names}."
        )
        raise SetUpError(message)
    return [field_ids[name] for name in wanted.fields]


def view_differences(view: BoardView, wanted: ViewInFile) -> tuple[str, ...]:
    lines: list[str] = []
    if view.layout != wanted.layout:
        lines.append(
            f"The view {view.name!r} has the layout {view.layout}, not {wanted.layout}."
        )
    if (view.filter or "") != wanted.filter:
        lines.append(
            f"The view {view.name!r} has the filter {view.filter or ''!r},"
            f" not {wanted.filter!r}."
        )
    # GitHub hands back a view's visible fields in the board's order of fields, not
    # the order they were set in.
    shown = {f.name for f in view.fields.nodes}
    if shown != set(wanted.fields):
        lines.append(
            f"The view {view.name!r} shows the fields {sorted(shown)},"
            f" not {sorted(wanted.fields)}."
        )
    return tuple(lines)


def create_view(
    graphql: GraphQL, board_id: str, wanted: ViewInFile, field_ids: list[str]
) -> Change:
    async def apply() -> None:
        ids: list[JsonValue] = list(field_ids)
        variables: dict[str, JsonValue] = {
            "projectId": board_id,
            "name": wanted.name,
            "layout": wanted.layout,
            "fieldIds": ids,
        }
        reply = await ask(graphql, CREATE_VIEW, variables, CreateViewReply)
        # GitHub's API takes no filter when it creates a view.
        view_id = reply.create_project_v2_view.project_v2_view.id
        await update_view(graphql, view_id, wanted, field_ids)()

    return Change((f"The view {wanted.name!r} is missing. It gets created.",), apply)


def update_view(
    graphql: GraphQL, view_id: str, wanted: ViewInFile, field_ids: list[str]
) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        ids: list[JsonValue] = list(field_ids)
        variables: dict[str, JsonValue] = {
            "viewId": view_id,
            "layout": wanted.layout,
            "filter": wanted.filter,
            "fieldIds": ids,
        }
        await ask(graphql, UPDATE_VIEW, variables, UpdateViewReply)

    return apply


def delete_view(graphql: GraphQL, view_id: str) -> Callable[[], Awaitable[None]]:
    async def apply() -> None:
        await ask(graphql, DELETE_VIEW, {"viewId": view_id}, DeleteViewReply)

    return apply
