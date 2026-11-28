"""A fake GitHub for tests: it answers the workflow's GraphQL requests from its state.

Each request is answered by the handler named after the request's operation, such as
`ReadIssue`. A handler hands back the reply's data, shaped as GitHub's would be.
"""

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from software_factory.config import factory_config
from software_factory.github.api import GitHubError, Repo

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from pydantic import JsonValue

REPO = Repo(owner="nimbusscale", name="dust-law")

type Handler = Callable[[Mapping[str, JsonValue]], JsonValue]


@dataclass
class FakeIssue:
    number: int
    title: str
    body: str

    @property
    def id(self) -> str:
        return f"I_{self.number}"


@dataclass
class FakePullRequest:
    number: int
    base: str
    head: str
    title: str
    body: str
    # The numbers of the issues the PR closes.
    closes: list[int] = field(default_factory=list)

    @property
    def id(self) -> str:
        return f"PR_{self.number}"


@dataclass(frozen=True)
class FakeOption:
    id: str
    name: str
    color: str = "GRAY"
    description: str = ""


def starting_options() -> list[FakeOption]:
    names = ["Todo", "In development", "In review", "Needs attention", "Done"]
    return [FakeOption(id=f"opt-{i}", name=name) for i, name in enumerate(names)]


@dataclass
class FakeBoard:
    number: int = field(default_factory=lambda: factory_config().board.number)
    id: str = "PVT_board"
    title: str = "dust-law"
    field_id: str = "PVTSSF_status"
    options: list[FakeOption] = field(default_factory=starting_options)
    has_status_field: bool = True
    # Each issue's node ID, and the ID of the status option its item is in, or None.
    items: dict[str, str | None] = field(default_factory=dict)

    def status_of(self, issue: FakeIssue) -> str | None:
        option_id = self.items.get(issue.id)
        return next((o.name for o in self.options if o.id == option_id), None)


@dataclass
class FakeGitHub:
    issues: list[FakeIssue] = field(default_factory=list)
    boards: list[FakeBoard] = field(default_factory=lambda: [FakeBoard()])
    default_branch: str = "main"
    pull_requests: list[FakePullRequest] = field(default_factory=list)
    # The comments on each issue or PR, by its node ID.
    comments: dict[str, list[str]] = field(default_factory=dict)
    # The operations whose replies don't fit their schemas, such as `ReadIssue`.
    broken: set[str] = field(default_factory=set)
    # The name of each operation asked for, in order.
    operations: list[str] = field(default_factory=list)

    async def __call__(
        self, query: str, variables: Mapping[str, JsonValue]
    ) -> JsonValue:
        match = re.search(r"\b(?:query|mutation)\s+(\w+)", query)
        if match is None:
            message = f"A request with no operation name: {query}"
            raise BadRequestError(message)
        operation = match.group(1)
        self.operations.append(operation)
        if operation in self.broken:
            return {"data": {"unexpected": True}}
        handlers: dict[str, Handler] = {
            "ReadIssue": self.read_issue,
            "AddComment": self.add_comment,
            "ReadBoard": self.read_board,
            "AddItem": self.add_item,
            "SetItemStatus": self.set_item_status,
            "ReadRepo": self.read_repo,
            "CreatePullRequest": self.create_pull_request,
            "ReadPullRequest": self.read_pull_request,
        }
        return {"data": handlers[operation](variables)}

    @property
    def board(self) -> FakeBoard:
        """The board the factory's config names."""
        number = factory_config().board.number
        return next(board for board in self.boards if board.number == number)

    def issue(self, number: int) -> FakeIssue:
        return next(issue for issue in self.issues if issue.number == number)

    def read_issue(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        issue = self.issue(integer(variables, "number"))
        node: dict[str, JsonValue] = {
            "id": issue.id,
            "number": issue.number,
            "title": issue.title,
            "body": issue.body,
        }
        return {"repository": {"issue": node}}

    def add_comment(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        subject_comments = self.comments.setdefault(text(variables, "subjectId"), [])
        subject_comments.append(text(variables, "body"))
        node_id = f"IC_{len(subject_comments)}"
        return {"addComment": {"commentEdge": {"node": {"id": node_id}}}}

    def read_board(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        number = integer(variables, "number")
        board = next((b for b in self.boards if b.number == number), None)
        if board is None:
            # The GitHub CLI fails on the error GitHub sends with the reply.
            message = f"Could not resolve to a ProjectV2 with the number {number}."
            raise GitHubError(message)
        node: dict[str, JsonValue] = {
            "id": board.id,
            "title": board.title,
            "field": (
                {"id": board.field_id, "options": json_options(board)}
                if board.has_status_field
                else None
            ),
        }
        return {"repositoryOwner": {"projectV2": node}}

    def add_item(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        expect("the board's ID", holds=text(variables, "projectId") == self.board.id)
        self.board.items.setdefault(text(variables, "contentId"), None)
        item_id = f"PVTI_{text(variables, 'contentId')}"
        return {"addProjectV2ItemById": {"item": {"id": item_id}}}

    def set_item_status(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        expect(
            "the field's ID", holds=text(variables, "fieldId") == self.board.field_id
        )
        item_id = text(variables, "itemId")
        option_id = text(variables, "optionId")
        expect("an option's ID", holds=option_id in {o.id for o in self.board.options})
        self.board.items[item_id.removeprefix("PVTI_")] = option_id
        return {"updateProjectV2ItemFieldValue": {"projectV2Item": {"id": item_id}}}

    def read_repo(self, _: Mapping[str, JsonValue]) -> JsonValue:
        branch: dict[str, JsonValue] = {"name": self.default_branch}
        return {"repository": {"id": "R_repo", "defaultBranchRef": branch}}

    def create_pull_request(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        expect("the repo's ID", holds=text(variables, "repositoryId") == "R_repo")
        pull_request = FakePullRequest(
            number=100 + len(self.pull_requests),
            base=text(variables, "base"),
            head=text(variables, "head"),
            title=text(variables, "title"),
            body=text(variables, "body"),
        )
        self.pull_requests.append(pull_request)
        url = f"https://github.com/{REPO}/pull/{pull_request.number}"
        node: dict[str, JsonValue] = {
            "id": pull_request.id,
            "number": pull_request.number,
            "url": url,
        }
        return {"createPullRequest": {"pullRequest": node}}

    def read_pull_request(self, variables: Mapping[str, JsonValue]) -> JsonValue:
        number = integer(variables, "number")
        pull_request = next(p for p in self.pull_requests if p.number == number)
        closing = [self.issue(n) for n in pull_request.closes]
        nodes: list[JsonValue] = [{"body": issue.body} for issue in closing[:2]]
        node: dict[str, JsonValue] = {
            "id": pull_request.id,
            "number": pull_request.number,
            "url": f"https://github.com/{REPO}/pull/{pull_request.number}",
            "baseRefName": pull_request.base,
            "closingIssuesReferences": {"totalCount": len(closing), "nodes": nodes},
        }
        return {"repository": {"pullRequest": node}}


def json_options(board: FakeBoard) -> list[JsonValue]:
    return [
        {"id": o.id, "name": o.name, "color": o.color, "description": o.description}
        for o in board.options
    ]


class BadRequestError(Exception):
    """A request that GitHub would refuse, which is a bug in the code that sent it."""


def expect(what: str, *, holds: bool) -> None:
    if not holds:
        message = f"The request doesn't hold {what}."
        raise BadRequestError(message)


def text(variables: Mapping[str, JsonValue], name: str) -> str:
    value = variables[name]
    if not isinstance(value, str):
        message = f"{name} isn't text: {value!r}"
        raise BadRequestError(message)
    return value


def integer(variables: Mapping[str, JsonValue], name: str) -> int:
    value = variables[name]
    if not isinstance(value, int):
        message = f"{name} isn't a whole number: {value!r}"
        raise BadRequestError(message)
    return value
