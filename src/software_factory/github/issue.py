from typing import TYPE_CHECKING

from software_factory.github.api import GraphQL, Reply, Repo, ask

if TYPE_CHECKING:
    from pydantic import JsonValue

READ_ISSUE = """
query ReadIssue($owner: String!, $name: String!, $number: Int!) {
  repository(owner: $owner, name: $name) {
    issue(number: $number) { id number title body }
  }
}
"""

ADD_COMMENT = """
mutation AddComment($subjectId: ID!, $body: String!) {
  addComment(input: {subjectId: $subjectId, body: $body}) {
    commentEdge { node { id } }
  }
}
"""


class Issue(Reply):
    # GitHub's node ID, which the API's mutations take.
    id: str
    number: int
    title: str
    body: str


class IssueRepository(Reply):
    issue: Issue


class ReadIssueReply(Reply):
    repository: IssueRepository


class CommentNode(Reply):
    id: str


class CommentEdge(Reply):
    node: CommentNode


class AddedComment(Reply):
    comment_edge: CommentEdge


class AddCommentReply(Reply):
    add_comment: AddedComment


async def read_issue(graphql: GraphQL, repo: Repo, number: int) -> Issue:
    variables: dict[str, JsonValue] = {
        "owner": repo.owner,
        "name": repo.name,
        "number": number,
    }
    reply = await ask(graphql, READ_ISSUE, variables, ReadIssueReply)
    return reply.repository.issue


async def post_comment(graphql: GraphQL, subject_id: str, body: str) -> None:
    """Posts a comment on the issue or PR whose node ID is `subject_id`."""
    variables: dict[str, JsonValue] = {"subjectId": subject_id, "body": body}
    await ask(graphql, ADD_COMMENT, variables, AddCommentReply)
