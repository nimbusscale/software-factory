from datetime import UTC, datetime
from pathlib import Path

import pytest

from software_factory.github.api import Repo
from software_factory.loop.command import factory_home, parse_request


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
