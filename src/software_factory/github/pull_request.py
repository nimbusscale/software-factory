from dataclasses import dataclass
from typing import TYPE_CHECKING

from software_factory.github.api import GraphQL, Reply, Repo, ask
from software_factory.github.board import Moment, move_issue
from software_factory.github.issue import Issue, post_comment

if TYPE_CHECKING:
    from collections.abc import Sequence

    from pydantic import JsonValue

    from software_factory.roles.implementer import DeclinedFinding, ImplementerResult
    from software_factory.roles.quality_reviewer import DroppedCandidate, Finding

READ_REPO = """
query ReadRepo($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) { id defaultBranchRef { name } }
}
"""

CREATE_PULL_REQUEST = """
mutation CreatePullRequest(
  $repositoryId: ID!, $base: String!, $head: String!, $title: String!, $body: String!
) {
  createPullRequest(input: {
    repositoryId: $repositoryId, baseRefName: $base, headRefName: $head,
    title: $title, body: $body
  }) {
    pullRequest { id number url }
  }
}
"""

NONE = "None."


@dataclass(frozen=True)
class NumberedFinding:
    # Such as `R2-F3`, the third finding of round 2 (TD-12).
    finding_id: str
    finding: Finding


@dataclass(frozen=True)
class RunRecord:
    """What a run keeps for its PR."""

    issue: Issue
    run_branch: str
    last_result: ImplementerResult
    # From every one of the implementer's results (TD-5).
    declined: Sequence[DeclinedFinding]
    # From every round.
    findings: Sequence[NumberedFinding]
    # The IDs of the findings the workflow gave the implementer.
    given: frozenset[str]
    # From every round.
    dropped: Sequence[DroppedCandidate]

    def not_given(self) -> list[NumberedFinding]:
        """Meets FR-25."""
        return [
            numbered
            for numbered in self.findings
            if numbered.finding.mark in {"nit", "pre_existing"}
            and numbered.finding_id not in self.given
        ]

    def to_check(self) -> list[NumberedFinding]:
        return [n for n in self.findings if n.finding.mark == "to_check"]


class BranchRef(Reply):
    name: str


class Repository(Reply):
    id: str
    default_branch_ref: BranchRef


class ReadRepoReply(Reply):
    repository: Repository


class PullRequest(Reply):
    id: str
    number: int
    url: str


class CreatedPullRequest(Reply):
    pull_request: PullRequest


class CreatePullRequestReply(Reply):
    create_pull_request: CreatedPullRequest


async def open_pull_request(
    graphql: GraphQL, repo: Repo, record: RunRecord
) -> PullRequest:
    """Opens the run's PR, posts its comment, and moves the issue on the board.

    The run branch has to be pushed first.
    """
    variables: dict[str, JsonValue] = {"owner": repo.owner, "name": repo.name}
    repository = (await ask(graphql, READ_REPO, variables, ReadRepoReply)).repository
    variables = {
        "repositoryId": repository.id,
        "base": repository.default_branch_ref.name,
        "head": record.run_branch,
        "title": record.issue.title,
        "body": description(record),
    }
    reply = await ask(graphql, CREATE_PULL_REQUEST, variables, CreatePullRequestReply)
    pull_request = reply.create_pull_request.pull_request
    await post_comment(graphql, pull_request.id, review_comment(record))
    # Meets FR-28 and FR-29.
    moment = (
        Moment.PR_OPENED_WITH_FINDING_TO_CHECK
        if record.to_check()
        else Moment.PR_OPENED
    )
    await move_issue(graphql, repo, record.issue, moment)
    return pull_request


def description(record: RunRecord) -> str:
    """The PR's description. Leaves out each list that has nothing in it."""
    result = record.last_result
    # Meets FR-16 and TD-6.
    parts = [f"Closes #{record.issue.number}", result.summary]
    sections = {
        "Declined findings": declined_lines(record),
        "Doc and code disagreements": [
            f"- **{d.item_id}**, in {d.code}: {d.disagreement}"
            for d in result.disagreements
        ],
        "Decisions on open points": [
            f"- On this text:\n\n  > {d.text}\n\n  It left unclear: {d.unclear}\n\n"
            f"  The implementer chose: {d.decision}"
            for d in result.decisions
        ],
        "Missing reasons": [
            f"- What's the reason for this decision?\n\n  > {m.decision}\n\n"
            f"  {suggestion(m.suggested_reason)}"
            for m in result.missing_reasons
        ],
    }
    parts.extend(
        f"## {heading}\n\n" + "\n".join(lines)
        for heading, lines in sections.items()
        if lines
    )
    return "\n\n".join(parts) + "\n"


def declined_lines(record: RunRecord) -> list[str]:
    """Meets FR-18."""
    findings = {n.finding_id: n.finding for n in record.findings}
    lines = []
    for declined in record.declined:
        finding = findings.get(declined.finding_id)
        about = (
            "no review reported a finding with this ID."
            if finding is None
            else f"`{finding.file}:{finding.line}`: {finding.problem}"
        )
        lines.append(
            f"- **{declined.finding_id}**, {about}\n\n"
            f"  Declined because: {declined.reason}"
        )
    return lines


def suggestion(suggested_reason: str | None) -> str:
    if suggested_reason is None:
        return "The implementer has no reason to suggest."
    return f"The implementer suggests: {suggested_reason}"


def review_comment(record: RunRecord) -> str:
    """The comment on the PR. Says None. for a list that has nothing in it.

    Meets FR-25, FR-30 and FR-31.
    """
    not_given = [
        f"- **{n.finding_id}**, a {MARK_NAMES[n.finding.mark]}, {where(n.finding)}:"
        f" {n.finding.problem}"
        for n in record.not_given()
    ]
    to_check = [
        f"- **{n.finding_id}**, {where(n.finding)}: {n.finding.problem}"
        for n in record.to_check()
    ]
    dropped = [
        f"- `{d.file}:{d.line}`: {d.problem}\n\n"
        f"  Dropped because {DROPPED_AS[d.dropped_as]}: {d.reason}"
        for d in record.dropped
    ]
    sections = {
        "Nits and pre-existing findings the implementer didn't get": not_given,
        "Findings to check": to_check,
        "Dropped candidates": dropped,
    }
    return (
        "\n\n".join(
            f"## {heading}\n\n" + ("\n".join(lines) if lines else NONE)
            for heading, lines in sections.items()
        )
        + "\n"
    )


MARK_NAMES = {
    "important": "important finding",
    "pre_existing": "pre-existing finding",
    "nit": "nit",
    "to_check": "finding to check",
}

DROPPED_AS = {
    "false_claim": "the claim is false",
    "older_note": "it's a note about a problem that was there before the change",
}


def where(finding: Finding) -> str:
    return f"`{finding.file}:{finding.line}`"
