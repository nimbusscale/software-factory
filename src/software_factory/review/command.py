"""The review command (FR-47).

It runs only in an SFE, which `tools/run-sfe.sh --review` starts with the command's
arguments.
"""

import argparse
import asyncio
import os
import sys

from claude_agent_sdk import query

from software_factory.github.api import Repo, gh_graphql
from software_factory.loop.command import AGENT_LIST, RUN_FOLDER
from software_factory.loop.run import github_remote
from software_factory.review.review import (
    ReviewEndedError,
    ReviewRequest,
    ReviewServices,
    review_pull_request,
)
from software_factory.roles.run import RoleRunner


def parse_request(argv: list[str] | None = None) -> ReviewRequest:
    parser = argparse.ArgumentParser(
        description="Reviews one PR of a project with the factory's reviewers."
    )
    parser.add_argument("repo", help="the project's repo, owner/name")
    parser.add_argument("pull_request", type=int, help="the PR's number")
    args = parser.parse_args(argv)
    repo_text: str = args.repo
    try:
        repo = Repo.parse(repo_text)
    except ValueError as error:
        parser.error(str(error))
    number: int = args.pull_request
    return ReviewRequest(repo=repo, pull_request_number=number)


def from_environment(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"The review didn't start. {name} isn't set. Start it in an SFE.")
    return value


def main() -> None:
    request = parse_request()
    # The GitHub CLI reads the same variable for the workflow's requests to GitHub.
    token = from_environment("GH_TOKEN")
    services = ReviewServices(
        graphql=gh_graphql,
        runner=RoleRunner(query, agent_list=RUN_FOLDER / AGENT_LIST),
        remote=lambda repo: github_remote(repo, token),
        factory_version=from_environment("FACTORY_VERSION"),
        run_folder=from_environment("FACTORY_RUN_FOLDER"),
    )
    try:
        review = asyncio.run(review_pull_request(request, services))
    except ReviewEndedError as error:
        sys.exit(f"The review didn't finish. {error}")
    sys.stdout.write(review.printed())
