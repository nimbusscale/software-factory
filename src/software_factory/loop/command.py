"""The implementation loop's command (FR-1).

It runs only in an SFE, which `tools/run-sfe.sh` starts with the command's arguments.
"""

import argparse
import asyncio
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from claude_agent_sdk import query

from software_factory.github.api import Repo, gh_graphql
from software_factory.github.pull_request import OpenedPullRequestError
from software_factory.loop.run import (
    RunEndedError,
    RunRefusedError,
    RunRequest,
    Services,
    github_remote,
    run,
)
from software_factory.roles.run import RoleRunner

# Where tools/run-sfe.sh mounts the run folder.
RUN_FOLDER = Path("/home/sfe/run")
AGENT_LIST = "agents.jsonl"


def factory_home() -> Path:
    """The folder that holds each run's working copy."""
    data_home = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local/share")
    return Path(data_home) / "software-factory"


def parse_request(argv: list[str] | None = None) -> RunRequest:
    parser = argparse.ArgumentParser(
        description="Runs the implementation loop on one issue of a project."
    )
    parser.add_argument("repo", help="the project's repo, owner/name")
    parser.add_argument("issue", type=int, help="the issue's number")
    parser.add_argument(
        "--rounds",
        type=int,
        help="the number of rounds, in place of the project's or the factory's",
    )
    args = parser.parse_args(argv)
    repo_text: str = args.repo
    try:
        repo = Repo.parse(repo_text)
    except ValueError as error:
        parser.error(str(error))
    issue: int = args.issue
    rounds: int | None = args.rounds
    return RunRequest(
        repo=repo, issue_number=issue, rounds=rounds, started_at=datetime.now(UTC)
    )


def from_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"The run didn't start. {name} isn't set. Start runs in an SFE.")
    return value


def main() -> None:
    request = parse_request()
    # The GitHub CLI reads the same variable for the workflow's requests to GitHub.
    token = from_environment("GH_TOKEN")
    services = Services(
        graphql=gh_graphql,
        runner=RoleRunner(query, agent_list=RUN_FOLDER / AGENT_LIST),
        home=factory_home(),
        remote=lambda repo: github_remote(repo, token),
        factory_version=from_environment("FACTORY_VERSION"),
        run_folder=from_environment("FACTORY_RUN_FOLDER"),
    )
    try:
        pull_request = asyncio.run(run(request, services))
    except RunRefusedError as error:
        sys.exit(f"The run didn't start. {error}")
    except RunEndedError as error:
        sys.exit(f"The run ended without a PR. {error}")
    except OpenedPullRequestError as error:
        sys.exit(str(error))
    sys.stdout.write(f"The run opened its PR: {pull_request.url}\n")
