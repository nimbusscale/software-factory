import asyncio

import pytest

from software_factory.config import factory_config
from software_factory.github.api import GitHubError
from software_factory.github.board import (
    STATUS_AT,
    Moment,
    end_without_pr,
    move_issue,
    set_board_statuses,
)
from software_factory.github.fake_github import (
    REPO,
    FakeBoard,
    FakeGitHub,
    FakeIssue,
    FakeOption,
)
from software_factory.github.issue import Issue, read_issue

TILES = FakeIssue(number=7, title="Add the tiles", body="## Why\n\nTiles.\n")


def github_with_issue() -> FakeGitHub:
    return FakeGitHub(issues=[TILES])


def issue_from(github: FakeGitHub) -> Issue:
    return asyncio.run(read_issue(github, REPO, TILES.number))


def test_run_start_moves_the_issue_to_in_development() -> None:
    github = github_with_issue()
    issue = issue_from(github)

    asyncio.run(move_issue(github, REPO, issue, Moment.RUN_STARTED))

    assert github.board.status_of(TILES) == "In development"


def test_moving_an_issue_on_the_board_again_changes_its_status() -> None:
    github = github_with_issue()
    issue = issue_from(github)

    asyncio.run(move_issue(github, REPO, issue, Moment.RUN_STARTED))
    asyncio.run(move_issue(github, REPO, issue, Moment.PR_OPENED))

    assert github.board.status_of(TILES) == "In review"
    assert list(github.board.items) == [TILES.id]


def test_run_that_ends_without_a_pr_says_why_and_needs_the_owner() -> None:
    github = github_with_issue()
    issue = issue_from(github)

    reason = "The implementer reached its turn cap of 100 turns."
    asyncio.run(end_without_pr(github, REPO, issue, reason))

    assert github.board.status_of(TILES) == "Needs attention"
    [comment] = github.comments[TILES.id]
    assert reason in comment


def test_each_moment_has_a_status_in_the_config() -> None:
    statuses = factory_config().statuses

    assert {statuses[STATUS_AT[moment]].name for moment in Moment} == {
        "In development",
        "In review",
        "Needs attention",
    }


def test_board_without_the_status_ends_the_run() -> None:
    board = FakeBoard(options=[FakeOption(id="opt-0", name="Todo")])
    github = FakeGitHub(issues=[TILES], boards=[board])
    issue = issue_from(github)

    with pytest.raises(GitHubError, match="no status 'In development'"):
        asyncio.run(move_issue(github, REPO, issue, Moment.RUN_STARTED))


@pytest.mark.parametrize("count", [0, 3])
def test_repo_without_exactly_one_board_ends_the_run(count: int) -> None:
    github = FakeGitHub(issues=[TILES], boards=[FakeBoard() for _ in range(count)])
    issue = issue_from(github)

    with pytest.raises(GitHubError, match=f"has {count} GitHub projects"):
        asyncio.run(move_issue(github, REPO, issue, Moment.RUN_STARTED))


def test_status_reply_that_doesnt_fit_its_schema_ends_the_run() -> None:
    github = FakeGitHub(issues=[TILES], broken={"SetItemStatus"})
    issue = issue_from(github)

    with pytest.raises(GitHubError, match="doesn't fit its schema"):
        asyncio.run(move_issue(github, REPO, issue, Moment.RUN_STARTED))


def test_board_statuses_are_set_from_the_config() -> None:
    github = github_with_issue()
    asyncio.run(set_board_statuses(github, REPO))

    statuses = factory_config().statuses.values()
    expected = {(s.name, s.color, s.description) for s in statuses}
    actual = {(o.name, o.color, o.description) for o in github.board.options}
    assert expected <= actual


def test_setting_board_statuses_keeps_the_boards_others_and_their_issues() -> None:
    github = github_with_issue()
    issue = issue_from(github)
    asyncio.run(move_issue(github, REPO, issue, Moment.PR_OPENED))
    before = list(github.board.options)

    asyncio.run(set_board_statuses(github, REPO))

    assert [(o.id, o.name) for o in github.board.options] == [
        (o.id, o.name) for o in before
    ]
    assert github.board.options[0] == before[0]
    assert github.board.status_of(TILES) == "In review"


def test_setting_board_statuses_adds_the_ones_the_board_lacks() -> None:
    board = FakeBoard(options=[FakeOption(id="opt-0", name="Todo")])
    github = FakeGitHub(boards=[board])

    asyncio.run(set_board_statuses(github, REPO))

    assert [o.name for o in github.board.options] == [
        "Todo",
        "In development",
        "In review",
        "Needs attention",
    ]
