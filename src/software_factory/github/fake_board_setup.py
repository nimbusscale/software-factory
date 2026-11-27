"""A fake GitHub for the board setup's tests: an owner's boards and their linked repos.

A board it creates starts with the settings GitHub gives a new board, as seen on
2026-11-27.
"""

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from software_factory.config import factory_config
from software_factory.github.fake_github import BadRequestError, expect, integer, text

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from pydantic import JsonValue

type Handler = Callable[[Mapping[str, JsonValue]], JsonValue]

FIELD_NAMES = [
    "Title",
    "Assignees",
    "Status",
    "Labels",
    "Linked pull requests",
    "Milestone",
    "Repository",
    "Reviewers",
    "Parent issue",
    "Sub-issues progress",
]

WORKFLOW_NAMES = [
    "Auto-add sub-issues to project",
    "Auto-close issue",
    "Item added to project",
    "Item closed",
    "Pull request linked to issue",
    "Pull request merged",
]

DEFAULT_LABELS = [
    ("bug", "d73a4a", "Something isn't working"),
    ("documentation", "0075ca", "Improvements or additions to documentation"),
    ("question", "d876e3", "Further information is requested"),
    ("wontfix", "ffffff", "This will not be worked on"),
]


@dataclass
class FakeOption:
    name: str
    color: str
    description: str
    id: str = field(default_factory=lambda: next_id("opt"))


def new_board_options() -> list[FakeOption]:
    return [
        FakeOption("Todo", "GREEN", "This item hasn't been started"),
        FakeOption("In Progress", "YELLOW", "This is actively being worked on"),
        FakeOption("Done", "PURPLE", "This has been completed"),
    ]


@dataclass
class FakeView:
    name: str
    layout: str
    filter: str | None
    field_ids: list[str]
    id: str = field(default_factory=lambda: next_id("view"))


@dataclass
class FakeLabel:
    name: str
    color: str
    description: str
    id: str = field(default_factory=lambda: next_id("label"))


def default_labels() -> list[FakeLabel]:
    return [FakeLabel(*label) for label in DEFAULT_LABELS]


@dataclass
class FakeRepo:
    name_with_owner: str
    labels: list[FakeLabel] = field(default_factory=default_labels)
    id: str = field(default_factory=lambda: next_id("repo"))


@dataclass
class FakeSetupBoard:
    number: int = field(default_factory=lambda: factory_config().board.number)
    title: str = "Factory"
    closed: bool = False
    options: list[FakeOption] = field(default_factory=new_board_options)
    # Each field's ID by its name.
    fields: dict[str, str] = field(
        default_factory=lambda: {name: f"field-{name}" for name in FIELD_NAMES}
    )
    views: list[FakeView] = field(default_factory=list)
    workflows: dict[str, str] = field(
        default_factory=lambda: {f"wf-{name}": name for name in WORKFLOW_NAMES}
    )
    repos: list[FakeRepo] = field(default_factory=list)
    id: str = field(default_factory=lambda: next_id("board"))

    def __post_init__(self) -> None:
        if not self.views:
            shown = ["Title", "Assignees", "Status", "Linked pull requests"]
            ids = [self.fields[name] for name in shown]
            self.views.append(FakeView("View 1", "TABLE_LAYOUT", None, ids))


@dataclass
class FakeBoardOwner:
    boards: list[FakeSetupBoard] = field(default_factory=list)
    # The number GitHub gives the next board created.
    next_number: int = field(default_factory=lambda: factory_config().board.number)
    # The name of each operation asked for, in order.
    operations: list[str] = field(default_factory=list)

    async def __call__(
        self, query: str, variables: Mapping[str, JsonValue]
    ) -> JsonValue:
        match = re.search(r"\b(?:query|mutation)\s+(\w+)", query)
        if match is None:
            raise BadRequestError(query)
        operation = match.group(1)
        self.operations.append(operation)
        handlers: dict[str, Handler] = {
            "ReadOwnerBoards": self.read_owner_boards,
            "ReadBoard": self.read_board,
            "ReadBoardSettings": self.read_board_settings,
            "CreateBoard": self.create_board,
            "SetStatusOptions": self.set_status_options,
            "CreateView": self.create_view,
            "UpdateView": self.update_view,
            "DeleteView": self.delete_view,
            "DeleteWorkflow": self.delete_workflow,
            "CreateLabel": self.create_label,
            "UpdateLabel": self.update_label,
            "DeleteLabel": self.delete_label,
        }
        return {"data": handlers[operation](variables)}

    @property
    def board(self) -> FakeSetupBoard:
        return self.boards[0]

    def numbered(self, variables: Mapping[str, JsonValue]) -> FakeSetupBoard:
        number = integer(variables, "number")
        return next(board for board in self.boards if board.number == number)

    def board_with(self, kind: str, item_id: str) -> FakeSetupBoard:
        for board in self.boards:
            ids = {
                "view": {view.id for view in board.views},
                "field": {f"status-{board.id}"},
                "workflow": set(board.workflows),
                "board": {board.id},
            }[kind]
            if item_id in ids:
                return board
        message = f"No {kind} {item_id}."
        raise BadRequestError(message)

    def read_owner_boards(self, _: Mapping[str, JsonValue]) -> JsonValue:
        nodes: list[JsonValue] = [
            {"number": b.number, "title": b.title, "closed": b.closed}
            for b in self.boards
        ]
        return {"repositoryOwner": {"id": "owner", "projectsV2": {"nodes": nodes}}}

    def read_board(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        board = self.numbered(variables)
        options: list[JsonValue] = [
            {"id": o.id, "name": o.name, "color": o.color, "description": o.description}
            for o in board.options
        ]
        status_field: dict[str, JsonValue] = {
            "id": f"status-{board.id}",
            "options": options,
        }
        node: dict[str, JsonValue] = {
            "id": board.id,
            "title": board.title,
            "field": status_field,
        }
        return {"repositoryOwner": {"projectV2": node}}

    def read_board_settings(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        board = self.numbered(variables)
        node: dict[str, JsonValue] = {
            "id": board.id,
            "fields": {"nodes": fields_json(board.fields)},
            "views": {"nodes": [view_json(board, view) for view in board.views]},
            "workflows": {
                "nodes": [{"id": i, "name": n} for i, n in board.workflows.items()]
            },
            "repositories": {"nodes": [repo_json(repo) for repo in board.repos]},
        }
        return {"repositoryOwner": {"projectV2": node}}

    def create_board(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        expect("the owner's ID", holds=text(variables, "ownerId") == "owner")
        board = FakeSetupBoard(number=self.next_number, title=text(variables, "title"))
        self.boards.append(board)
        return {"createProjectV2": {"projectV2": {"number": board.number}}}

    def set_status_options(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        board = self.board_with("field", text(variables, "fieldId"))
        options = variables["options"]
        if not isinstance(options, list):
            raise BadRequestError(str(options))
        new_options: list[FakeOption] = []
        for option in options:
            if not isinstance(option, dict):
                raise BadRequestError(str(option))
            fields = [text(option, name) for name in ("name", "color", "description")]
            new_option = FakeOption(*fields)
            if "id" in option:
                new_option.id = text(option, "id")
            new_options.append(new_option)
        board.options = new_options
        field_id = text(variables, "fieldId")
        return {"updateProjectV2Field": {"projectV2Field": {"id": field_id}}}

    def create_view(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        board = self.board_with("board", text(variables, "projectId"))
        view = FakeView(
            text(variables, "name"), text(variables, "layout"), None, ids(variables)
        )
        board.views.append(view)
        return {"createProjectV2View": {"projectV2View": {"id": view.id}}}

    def update_view(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        view_id = text(variables, "viewId")
        board = self.board_with("view", view_id)
        view = next(view for view in board.views if view.id == view_id)
        view.layout = text(variables, "layout")
        view.filter = text(variables, "filter")
        view.field_ids = ids(variables)
        return {"updateProjectV2View": {"projectV2View": {"id": view_id}}}

    def delete_view(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        view_id = text(variables, "viewId")
        board = self.board_with("view", view_id)
        expect("a view left on the board", holds=len(board.views) > 1)
        board.views = [view for view in board.views if view.id != view_id]
        return {"deleteProjectV2View": {"projectV2View": {"id": view_id}}}

    def delete_workflow(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        workflow_id = text(variables, "workflowId")
        del self.board_with("workflow", workflow_id).workflows[workflow_id]
        return {"deleteProjectV2Workflow": {"deletedWorkflowId": workflow_id}}

    def repo(self, repo_id: str) -> FakeRepo:
        repos = (repo for board in self.boards for repo in board.repos)
        return next(repo for repo in repos if repo.id == repo_id)

    def label(self, label_id: str) -> tuple[FakeRepo, FakeLabel]:
        repos = (repo for board in self.boards for repo in board.repos)
        labels = ((repo, label) for repo in repos for label in repo.labels)
        found = next(((r, x) for r, x in labels if x.id == label_id), None)
        if found is None:
            raise BadRequestError(label_id)
        return found

    def create_label(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        repo = self.repo(text(variables, "repositoryId"))
        fields = [text(variables, name) for name in ("name", "color", "description")]
        # As GitHub does, it takes names that differ only in case as the same.
        taken = {x.name.casefold() for x in repo.labels}
        expect("a name no label has", holds=fields[0].casefold() not in taken)
        label = FakeLabel(*fields)
        repo.labels.append(label)
        return {"createLabel": {"label": {"id": label.id}}}

    def update_label(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        repo, label = self.label(text(variables, "id"))
        name = text(variables, "name")
        others = (x.name.casefold() for x in repo.labels if x is not label)
        expect("a name no other label has", holds=name.casefold() not in others)
        label.name = name
        label.color = text(variables, "color")
        label.description = text(variables, "description")
        return {"updateLabel": {"label": {"id": label.id}}}

    def delete_label(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        repo, label = self.label(text(variables, "id"))
        repo.labels.remove(label)
        return {"deleteLabel": {"clientMutationId": None}}


def fields_json(fields: dict[str, str]) -> list[JsonValue]:
    return [{"id": field_id, "name": name} for name, field_id in fields.items()]


def view_json(board: FakeSetupBoard, view: FakeView) -> JsonValue:
    # As GitHub does, it lists the visible fields in the board's order of fields.
    shown: list[JsonValue] = [
        {"name": name}
        for name, field_id in board.fields.items()
        if field_id in view.field_ids
    ]
    return {
        "id": view.id,
        "name": view.name,
        "layout": view.layout,
        "filter": view.filter,
        "fields": {"nodes": shown},
    }


def repo_json(repo: FakeRepo) -> JsonValue:
    labels: list[JsonValue] = [
        {"id": x.id, "name": x.name, "color": x.color, "description": x.description}
        for x in repo.labels
    ]
    return {
        "id": repo.id,
        "nameWithOwner": repo.name_with_owner,
        "labels": {"nodes": labels},
    }


def ids(variables: Mapping[str, JsonValue]) -> list[str]:
    value = variables["fieldIds"]
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise BadRequestError(str(value))
    return [v for v in value if isinstance(v, str)]


_counter = iter(range(1, 1_000_000))


def next_id(prefix: str) -> str:
    return f"{prefix}-{next(_counter)}"
