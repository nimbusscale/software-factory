from typing import TYPE_CHECKING

from software_factory.github.api import GraphQL, Reply, Repo, ask

if TYPE_CHECKING:
    from pydantic import JsonValue

# Two closing issues at most, since TR-26 only needs to know whether there's one.
READ_PULL_REQUEST = """
query ReadPullRequest($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      id number url baseRefName
      closingIssuesReferences(first: 2) { totalCount nodes { body } }
    }
  }
}
"""


class ClosingIssue(Reply):
    body: str


class ClosingIssues(Reply):
    total_count: int
    nodes: list[ClosingIssue]


class PullRequestToReview(Reply):
    # GitHub's node ID, which the API's mutations take.
    id: str
    number: int
    url: str
    base_ref_name: str
    closing_issues_references: ClosingIssues

    def issue_body(self) -> str | None:
        """The body of the issue the PR closes, or None (TR-26)."""
        closing = self.closing_issues_references
        if closing.total_count != 1:
            return None
        return closing.nodes[0].body


class PullRequestRepository(Reply):
    pull_request: PullRequestToReview


class ReadPullRequestReply(Reply):
    repository: PullRequestRepository


async def read_pull_request(
    graphql: GraphQL, repo: Repo, number: int
) -> PullRequestToReview:
    variables: dict[str, JsonValue] = {
        "owner": repo.owner,
        "name": repo.name,
        "number": number,
    }
    reply = await ask(graphql, READ_PULL_REQUEST, variables, ReadPullRequestReply)
    return reply.repository.pull_request
