import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from software_factory.github.api import GitHubError, Repo
from software_factory.github.pull_request import OpenedPullRequestError, PullRequest
from software_factory.loop import command
from software_factory.loop.command import factory_home, parse_request
from software_factory.loop.run import RunEndedError, RunRefusedError

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from software_factory.loop.run import RunRequest, Services


@pytest.fixture(autouse=True)
def sfe_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """The variables the SFE sets for the command."""
    monkeypatch.setenv("GH_TOKEN", "token-for-github")
    monkeypatch.setenv("FACTORY_VERSION", "0123456789ab")


def test_command_reads_the_repo_issue_and_rounds() -> None:
    before = datetime.now(UTC)

    request = parse_request(["nimbusscale/dust-law", "7", "--rounds", "2"])

    assert request.repo == Repo(owner="nimbusscale", name="dust-law")
    assert (request.issue_number, request.rounds) == (7, 2)
    assert before <= request.started_at <= datetime.now(UTC)


def test_command_without_rounds_leaves_them_to_the_settings() -> None:
    assert parse_request(["nimbusscale/dust-law", "7"]).rounds is None


def test_command_refuses_a_repo_that_isnt_owner_and_name() -> None:
    with pytest.raises(SystemExit):
        parse_request(["dust-law", "7"])


def test_factory_home_follows_xdg_data_home(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("XDG_DATA_HOME", "/data")

    assert factory_home() == Path("/data/software-factory")


def test_factory_home_without_xdg_data_home_is_in_local_share(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)
    monkeypatch.setenv("HOME", "/home/owner")

    assert factory_home() == Path("/home/owner/.local/share/software-factory")


def pull_request() -> PullRequest:
    url = "https://github.com/nimbusscale/dust-law/pull/100"
    return PullRequest(id="PR_100", number=100, url=url)


def fake_run(
    outcome: PullRequest | Exception,
) -> Callable[[RunRequest, Services], Awaitable[PullRequest]]:
    async def run(_request: RunRequest, _services: Services) -> PullRequest:
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return run


@pytest.mark.parametrize(
    "case",
    [
        (RunRefusedError("No rounds."), "The run didn't start. No rounds."),
        (RunEndedError("No result."), "The run ended without a PR. No result."),
        (
            OpenedPullRequestError(pull_request(), GitHubError("No comment.")),
            (
                "The run opened its PR, https://github.com/nimbusscale/dust-law/pull/100,"
                " and then: No comment."
            ),
        ),
    ],
)
def test_command_says_why_a_run_ended(
    monkeypatch: pytest.MonkeyPatch, case: tuple[Exception, str]
) -> None:
    error, message = case
    monkeypatch.setattr(command, "run", fake_run(error))
    monkeypatch.setattr(
        sys, "argv", ["implementation-loop", "nimbusscale/dust-law", "7"]
    )

    with pytest.raises(SystemExit) as exited:
        command.main()

    assert exited.value.code == message


def test_command_prints_the_pr(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(command, "run", fake_run(pull_request()))
    monkeypatch.setattr(
        sys, "argv", ["implementation-loop", "nimbusscale/dust-law", "7"]
    )

    command.main()

    assert capsys.readouterr().out == (
        "The run opened its PR: https://github.com/nimbusscale/dust-law/pull/100\n"
    )
