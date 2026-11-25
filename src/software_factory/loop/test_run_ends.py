import shutil
from typing import TYPE_CHECKING

import pytest

from software_factory.github.pull_request import OpenedPullRequestError
from software_factory.loop.conftest import (
    ISSUE_NUMBER,
    board_status,
    fake_github,
    finding,
    implementer_turn,
    push_settings,
    reviewer_turn,
    services,
    start_run,
)
from software_factory.loop.run import RunEndedError, RunRefusedError
from software_factory.roles.fake_agent_sdk import (
    RawMessage,
    ScriptedQuery,
    result_message,
    saved_response,
)

if TYPE_CHECKING:
    from pathlib import Path

    from software_factory.github.fake_github import FakeGitHub


def issue_comments(github: FakeGitHub) -> list[str]:
    return github.comments.get(github.issue(ISSUE_NUMBER).id, [])


def assert_ended_without_pr(github: FakeGitHub, reason: str) -> None:
    """Meets FR-13 and FR-14."""
    assert not github.pull_requests
    assert board_status(github) == "Needs attention"
    [comment] = issue_comments(github)
    assert reason in comment


def test_role_with_no_result_ends_the_run(remote: Path, tmp_path: Path) -> None:
    roles = ScriptedQuery(
        [lambda _: saved_response("success_without_structured_output")]
    )
    github = fake_github()

    with pytest.raises(RunEndedError, match="without handing back a result"):
        start_run(services(github, roles, remote, tmp_path / "home"))

    assert_ended_without_pr(github, "The implementer ended without handing back")
    # TR-8.
    assert not any((tmp_path / "home" / "working-copies").rglob("*.*"))


def test_result_that_doesnt_fit_its_schema_ends_the_run(
    remote: Path, tmp_path: Path
) -> None:
    def reviewer_with_no_findings_field(_: Path) -> list[RawMessage]:
        return [result_message(structured_output={"status": "done", "reason": "."})]

    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_with_no_findings_field,
        ]
    )
    github = fake_github()

    with pytest.raises(RunEndedError, match="doesn't fit its result schema"):
        start_run(services(github, roles, remote, tmp_path / "home"))

    assert_ended_without_pr(github, "The quality reviewer's result doesn't fit")


def test_failed_git_command_ends_the_run(remote: Path, tmp_path: Path) -> None:
    def implementer_that_loses_the_remote(cwd: Path) -> list[RawMessage]:
        shutil.rmtree(remote)
        return implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles")(cwd)

    roles = ScriptedQuery([implementer_that_loses_the_remote, reviewer_turn([])])
    github = fake_github()

    with pytest.raises(RunEndedError, match="git push"):
        start_run(services(github, roles, remote, tmp_path / "home"))

    assert_ended_without_pr(github, "git push")


def test_work_that_changes_nothing_ends_the_run(remote: Path, tmp_path: Path) -> None:
    roles = ScriptedQuery([implementer_turn({}, "Nothing")])
    github = fake_github()

    with pytest.raises(RunEndedError, match="without changing any file"):
        start_run(services(github, roles, remote, tmp_path / "home"))

    assert_ended_without_pr(github, "without changing any file")


class RoleCrashError(Exception):
    pass


def test_error_the_workflow_doesnt_handle_ends_the_run(
    remote: Path, tmp_path: Path
) -> None:
    def crash(_: Path) -> list[RawMessage]:
        raise RoleCrashError

    github = fake_github()

    with pytest.raises(RoleCrashError):
        start_run(services(github, ScriptedQuery([crash]), remote, tmp_path / "home"))

    assert_ended_without_pr(github, "an error it doesn't handle: RoleCrashError()")


def test_reply_that_doesnt_fit_after_the_pr_opens_leaves_the_board(
    remote: Path, tmp_path: Path
) -> None:
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_turn([finding("nit", "A name could be clearer.")]),
        ]
    )
    github = fake_github()
    github.broken.add("AddComment")

    with pytest.raises(OpenedPullRequestError):
        start_run(services(github, roles, remote, tmp_path / "home"))

    assert len(github.pull_requests) == 1
    assert board_status(github) == "In development"


@pytest.mark.parametrize(
    "case",
    [
        # FR-5.
        ("rounds = 0\n", "rounds: Input should be greater than or equal to 1"),
        # FR-26.
        ('rounds = "3"\n', "rounds: Input should be a valid integer"),
        ("rounds = 2.0\n", "rounds: Input should be a valid integer"),
        ("[turn_caps]\nimplementer = -1\n", "turn_caps.implementer: Input should"),
        ("round = 2\n", "round: Extra inputs are not permitted"),
        ("rounds = \n", "isn't valid TOML"),
    ],
)
def test_setting_that_isnt_valid_refuses_the_run(
    remote: Path, author: Path, tmp_path: Path, case: tuple[str, str]
) -> None:
    settings_file, reason = case
    push_settings(author, settings_file)
    github = fake_github()

    with pytest.raises(RunRefusedError, match=reason):
        start_run(services(github, ScriptedQuery([]), remote, tmp_path / "home"))

    assert github.operations == []


def test_fewer_than_1_round_from_the_command_refuses_the_run(
    remote: Path, tmp_path: Path
) -> None:
    github = fake_github()

    with pytest.raises(RunRefusedError, match="at least 1 round"):
        start_run(
            services(github, ScriptedQuery([]), remote, tmp_path / "home"), rounds=0
        )

    assert github.operations == []


def test_issue_that_cant_be_read_refuses_the_run(remote: Path, tmp_path: Path) -> None:
    github = fake_github()
    github.broken.add("ReadIssue")

    with pytest.raises(RunRefusedError, match="doesn't fit its schema"):
        start_run(services(github, ScriptedQuery([]), remote, tmp_path / "home"))

    assert github.operations == ["ReadIssue"]
