import asyncio
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from software_factory.github.api import GitHubError
from software_factory.github.fake_github import REPO, FakeGitHub, FakeIssue
from software_factory.github.issue import read_issue
from software_factory.github.pull_request import (
    NumberedFinding,
    OpenedPullRequestError,
    RunRecord,
    description,
    open_pull_request,
    review_comment,
)
from software_factory.roles.implementer import (
    Decision,
    DeclinedFinding,
    DocCodeDisagreement,
    ImplementerResult,
    MissingReason,
)
from software_factory.roles.quality_reviewer import DroppedCandidate, Finding

if TYPE_CHECKING:
    from software_factory.github.pull_request import PullRequest

TILES = FakeIssue(number=7, title="Add the tiles", body="## Why\n\nTiles.\n")
RUN_BRANCH = "factory/issue-7-20261124-213000"
VERSION = "0123456789ab"

LAST_RESULT = ImplementerResult(
    summary="Adds the tile deck and deals four tiles to each player.",
    declined=[],
    disagreements=[
        DocCodeDisagreement(
            item_id="FR-3",
            code="`deal` in `src/tiles.py`",
            disagreement="FR-3 says five tiles, and the code deals four.",
        )
    ],
    decisions=[
        Decision(
            text="Deal the tiles at the start.",
            unclear="Whether a player who joins late gets tiles.",
            decision="A late player gets four tiles, like the others.",
        )
    ],
    missing_reasons=[
        MissingReason(decision="The deck holds 40 tiles.", suggested_reason=None)
    ],
    commit_message="Deal the tiles",
)


def finding(finding_id: str, mark: str, problem: str) -> NumberedFinding:
    found = Finding.model_validate(
        {
            "file": "src/tiles.py",
            "line": 12,
            "label": "bug",
            "mark": mark,
            "problem": problem,
            "failure_case": "A deck of 0 tiles.",
            "label_reason": "It crashes.",
        }
    )
    return NumberedFinding(finding_id=finding_id, finding=found)


IMPORTANT = finding("R1-F1", "important", "The deal skips the last player.")
NIT_GIVEN = finding("R1-F2", "nit", "The loop could be a comprehension.")
OLD_BUG = finding("R1-F3", "pre_existing", "The shuffle isn't seeded.")
NIT_LAST_ROUND = finding("R2-F1", "nit", "A name could be clearer.")
TO_CHECK = finding("R2-F2", "to_check", "Check the tile API sends 40 tiles.")

DROPPED = DroppedCandidate(
    file="src/tiles.py",
    line=30,
    problem="The deck can run out.",
    label="bug",
    dropped_as="false_claim",
    reason="The deck is refilled before each deal.",
)


def record(*findings: NumberedFinding) -> RunRecord:
    return RunRecord(
        issue=asyncio.run(read_issue(FakeGitHub(issues=[TILES]), REPO, 7)),
        run_branch=RUN_BRANCH,
        last_result=LAST_RESULT,
        declined=[DeclinedFinding(finding_id="R1-F2", reason="It reads better.")],
        findings=findings,
        given=frozenset({"R1-F1", "R1-F2"}),
        dropped=[DROPPED],
    )


def open_for(run: RunRecord) -> tuple[FakeGitHub, PullRequest]:
    github = FakeGitHub(issues=[TILES])
    pull_request = asyncio.run(open_pull_request(github, REPO, run, VERSION))
    return github, pull_request


def test_opens_the_pr_from_the_run_branch_with_the_issues_title() -> None:
    github, pull_request = open_for(record(IMPORTANT))

    [opened] = github.pull_requests
    assert (opened.base, opened.head, opened.title) == ("main", RUN_BRANCH, TILES.title)
    assert opened.body == description(record(IMPORTANT), VERSION)
    assert pull_request.number == opened.number


def test_description_closes_the_issue_and_holds_the_implementers_text() -> None:
    text = description(record(IMPORTANT, NIT_GIVEN), VERSION)

    assert text.startswith("Closes #7\n\n")
    assert LAST_RESULT.summary in text
    assert "**FR-3**, in `deal` in `src/tiles.py`: FR-3 says five tiles" in text
    assert "> Deal the tiles at the start." in text
    assert "Whether a player who joins late gets tiles." in text
    assert "A late player gets four tiles" in text
    assert "What's the reason for this decision?\n\n  > The deck holds 40" in text
    assert "no reason to suggest" in text


def test_description_lists_each_declined_finding_with_its_reason() -> None:
    text = description(record(IMPORTANT, NIT_GIVEN), VERSION)

    assert "**R1-F2**, `src/tiles.py:12`: The loop could be a comprehension." in text
    assert "Declined because: It reads better." in text


def test_declined_finding_no_review_reported_is_still_listed() -> None:
    text = description(record(IMPORTANT), VERSION)

    assert "**R1-F2**, no review reported a finding with this ID." in text


def test_description_gives_the_implementers_suggested_reason() -> None:
    reason = MissingReason(
        decision="The deck holds 40 tiles.", suggested_reason="40 fills the table."
    )
    result = LAST_RESULT.model_copy(update={"missing_reasons": [reason]})

    text = description(replace(record(IMPORTANT), last_result=result), VERSION)

    assert "The implementer suggests: 40 fills the table." in text


def test_text_with_a_blank_line_stays_in_its_list_item() -> None:
    decision = Decision(
        text="Deal the tiles.\n\nA late player waits.",
        unclear="Who deals.\n\nAnd when.",
        decision="The host deals.",
    )
    result = LAST_RESULT.model_copy(update={"decisions": [decision]})

    text = description(replace(record(IMPORTANT), last_result=result), VERSION)

    quoted = "  > Deal the tiles.\n  >\n  > A late player waits."
    assert quoted in text
    assert "It left unclear: Who deals.\n  \n  And when." in text


def test_description_leaves_out_empty_lists() -> None:
    result = LAST_RESULT.model_copy(
        update={"disagreements": [], "decisions": [], "missing_reasons": []}
    )
    run = record(IMPORTANT)
    empty = replace(run, last_result=result, declined=[])

    assert description(empty, VERSION) == (
        f"Closes #7\n\n{LAST_RESULT.summary}\n\n"
        "Made by factory version `0123456789ab`.\n"
    )


def test_description_names_the_factory_version() -> None:
    text = description(record(IMPORTANT), VERSION)

    # FR-33.
    assert text.endswith("\n\nMade by factory version `0123456789ab`.\n")


def test_comment_lists_the_findings_the_implementer_didnt_get() -> None:
    comment = review_comment(record(IMPORTANT, NIT_GIVEN, OLD_BUG, NIT_LAST_ROUND))

    assert "**R1-F3**, a pre-existing finding" in comment
    assert "**R2-F1**, a nit, `src/tiles.py:12`: A name could be clearer." in comment
    assert "R1-F1" not in comment
    assert "R1-F2" not in comment


def test_comment_lists_findings_to_check_and_dropped_candidates() -> None:
    comment = review_comment(record(IMPORTANT, TO_CHECK))

    assert "**R2-F2**, `src/tiles.py:12`: Check the tile API sends 40" in comment
    assert "`src/tiles.py:30`: The deck can run out." in comment
    assert "Dropped because the claim is false: The deck is refilled" in comment


def test_comment_says_why_a_repeat_of_an_earlier_finding_was_dropped() -> None:
    repeat = DroppedCandidate(
        file="src/tiles.py",
        line=12,
        problem="The shuffle isn't seeded.",
        label="F1",
        dropped_as="earlier_finding",
        reason="R1-F3, a pre-existing finding.",
    )
    comment = review_comment(replace(record(IMPORTANT), dropped=[repeat]))

    assert "Dropped because an earlier round already raised it: R1-F3" in comment


def test_comment_says_none_for_an_empty_list() -> None:
    run = record(IMPORTANT)
    comment = review_comment(replace(run, dropped=[]))

    assert comment.count("None.") == 3


def test_pr_gets_the_review_comment() -> None:
    run = record(IMPORTANT, TO_CHECK)
    github, pull_request = open_for(run)

    assert github.comments[pull_request.id] == [review_comment(run)]


def test_pr_with_no_finding_to_check_is_ready_for_the_owner() -> None:
    github, _ = open_for(record(IMPORTANT, OLD_BUG))

    assert github.board.status_of(TILES) == "In review"


def test_pr_with_a_finding_to_check_needs_the_owner() -> None:
    github, _ = open_for(record(IMPORTANT, TO_CHECK))

    assert github.board.status_of(TILES) == "Needs attention"


def test_pr_reply_that_doesnt_fit_its_schema_ends_the_run() -> None:
    github = FakeGitHub(issues=[TILES], broken={"CreatePullRequest"})

    with pytest.raises(GitHubError, match="doesn't fit its schema"):
        asyncio.run(open_pull_request(github, REPO, record(IMPORTANT), VERSION))
    assert github.board.status_of(TILES) is None


def test_failure_after_the_pr_opens_says_the_pr_is_open() -> None:
    github = FakeGitHub(issues=[TILES], broken={"AddComment"})

    with pytest.raises(OpenedPullRequestError, match="opened its PR") as error:
        asyncio.run(open_pull_request(github, REPO, record(IMPORTANT), VERSION))
    [opened] = github.pull_requests
    assert error.value.pull_request.number == opened.number
