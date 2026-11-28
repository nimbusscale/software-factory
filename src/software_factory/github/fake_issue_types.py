"""The issue types of a fake organization, for the board setup's tests.

An organization starts with the issue types GitHub gives a new one, as seen on
2026-11-28.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from software_factory.github.fake_github import BadRequestError, expect, text

if TYPE_CHECKING:
    from collections.abc import Mapping

    from pydantic import JsonValue

NEW_ORGANIZATION_ISSUE_TYPES = [
    ("Task", "YELLOW", "A specific piece of work"),
    ("Bug", "RED", "An unexpected problem or behavior"),
    ("Feature", "BLUE", "A request, idea, or new functionality"),
]

_counter = iter(range(1, 1_000_000))


def next_id() -> str:
    return f"type-{next(_counter)}"


@dataclass
class FakeIssueType:
    name: str
    color: str
    description: str
    is_enabled: bool = True
    id: str = field(default_factory=next_id)


def new_organization_issue_types() -> list[FakeIssueType]:
    return [FakeIssueType(*issue_type) for issue_type in NEW_ORGANIZATION_ISSUE_TYPES]


def find(types: list[FakeIssueType], type_id: str) -> FakeIssueType:
    found = next((t for t in types if t.id == type_id), None)
    if found is None:
        raise BadRequestError(type_id)
    return found


def create_issue_type(
    types: list[FakeIssueType], variables: Mapping[str, JsonValue]
) -> JsonValue:
    expect("the owner's ID", holds=text(variables, "ownerId") == "owner")
    name, color, description = (
        text(variables, key) for key in ("name", "color", "description")
    )
    taken = {t.name.casefold() for t in types}
    expect("a name no issue type has", holds=name.casefold() not in taken)
    issue_type = FakeIssueType(name, color, description)
    types.append(issue_type)
    return {"createIssueType": {"issueType": {"id": issue_type.id}}}


def update_issue_type(
    types: list[FakeIssueType], variables: Mapping[str, JsonValue]
) -> JsonValue:
    issue_type = find(types, text(variables, "id"))
    name = text(variables, "name")
    others = (t.name.casefold() for t in types if t is not issue_type)
    expect("a name no other issue type has", holds=name.casefold() not in others)
    issue_type.name = name
    issue_type.color = text(variables, "color")
    issue_type.description = text(variables, "description")
    issue_type.is_enabled = True
    return {"updateIssueType": {"issueType": {"id": issue_type.id}}}


def delete_issue_type(
    types: list[FakeIssueType], variables: Mapping[str, JsonValue]
) -> JsonValue:
    issue_type = find(types, text(variables, "id"))
    types.remove(issue_type)
    return {"deleteIssueType": {"deletedIssueTypeId": issue_type.id}}


def issue_type_json(issue_type: FakeIssueType) -> JsonValue:
    return {
        "id": issue_type.id,
        "name": issue_type.name,
        "color": issue_type.color,
        "description": issue_type.description,
        "isEnabled": issue_type.is_enabled,
    }


HANDLERS = {
    "CreateIssueType": create_issue_type,
    "UpdateIssueType": update_issue_type,
    "DeleteIssueType": delete_issue_type,
}
