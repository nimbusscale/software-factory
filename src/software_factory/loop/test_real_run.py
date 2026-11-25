"""The test of a whole run that calls Claude (CS-4).

Run it with `uv run pytest -m claude src`. It runs each role as the factory does, on
Opus, on a small project in a local git repo, with a fake GitHub.
"""

import asyncio
from pathlib import Path

import pytest
from claude_agent_sdk import query

from software_factory.conftest import run_git
from software_factory.github.fake_github import REPO, FakeGitHub, FakeIssue
from software_factory.loop.conftest import FACTORY_REPO, STARTED
from software_factory.loop.run import RunRequest, Services, run
from software_factory.roles.run import RoleRunner

# This checkout plays the factory's repo, so the roles get the doc standards on its
# main branch.
FACTORY_CHECKOUT = Path(__file__).parents[3]

ISSUE_BODY = """## Why

Players need to know how many people the game takes before they start.

## Design

None.

## Do

1. Add a line to `README.md` that says the game takes 2 to 4 players.

## Acceptance criteria

- `README.md` says the game takes 2 to 4 players.
"""


def set_up_project(author: Path) -> None:
    (author / "CLAUDE.md").write_text(
        "# A card game\n\nThe repo holds the game's rules, and no code.\n"
    )
    (author / "software-factory.toml").write_text(
        "rounds = 1\n\n[turn_caps]\nimplementer = 30\nquality_reviewer = 30\n"
    )
    run_git("add", "--all", cwd=author)
    run_git("commit", "--quiet", "--message", "Set up the project", cwd=author)
    run_git("push", "--quiet", "origin", "main", cwd=author)


@pytest.mark.claude
def test_run_opens_a_pr_for_the_work(
    author: Path, remote: Path, tmp_path: Path
) -> None:
    set_up_project(author)
    issue = FakeIssue(number=7, title="Say how many players", body=ISSUE_BODY)
    github = FakeGitHub(issues=[issue])
    services = Services(
        graphql=github,
        runner=RoleRunner(query),
        home=tmp_path / "home",
        remote_url=lambda repo: str(
            FACTORY_CHECKOUT if repo == FACTORY_REPO else remote
        ),
    )
    request = RunRequest(repo=REPO, issue_number=7, rounds=None, started_at=STARTED)

    pull_request = asyncio.run(run(request, services))

    [opened] = github.pull_requests
    assert opened.number == pull_request.number
    assert opened.body.startswith("Closes #7\n")
    readme = run_git("show", f"{opened.head}:README.md", cwd=remote)
    assert "2 to 4 players" in readme
    assert github.board.status_of(issue) in {"In review", "Needs attention"}
