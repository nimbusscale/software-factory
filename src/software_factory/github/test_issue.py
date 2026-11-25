import asyncio

import pytest

from software_factory.github.api import GitHubError
from software_factory.github.fake_github import REPO, FakeGitHub, FakeIssue
from software_factory.github.issue import Issue, post_comment, read_issue

TILES = FakeIssue(number=7, title="Add the tiles", body="## Why\n\nTiles.\n")


def github_with_issue() -> FakeGitHub:
    return FakeGitHub(issues=[TILES])


def issue_from(github: FakeGitHub) -> Issue:
    return asyncio.run(read_issue(github, REPO, TILES.number))


def test_reads_the_issues_title_and_body() -> None:
    issue = issue_from(github_with_issue())

    assert (issue.title, issue.body) == (TILES.title, TILES.body)


def test_issue_reply_that_doesnt_fit_its_schema_ends_the_run() -> None:
    github = FakeGitHub(issues=[TILES], broken={"ReadIssue"})

    with pytest.raises(GitHubError, match="doesn't fit its schema"):
        issue_from(github)


def test_posts_a_comment_on_the_issue() -> None:
    github = github_with_issue()
    issue = issue_from(github)

    asyncio.run(post_comment(github, issue.id, "Started."))

    assert github.comments == {TILES.id: ["Started."]}
