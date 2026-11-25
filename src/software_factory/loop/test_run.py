from typing import TYPE_CHECKING

from software_factory.conftest import run_git
from software_factory.loop.conftest import (
    IMPLEMENTER_SESSION,
    ISSUE_BODY,
    RUN_BRANCH,
    SeenReviewCopies,
    board_status,
    fake_github,
    finding,
    implementer_turn,
    push_settings,
    reviewer_turn,
    services,
    start_run,
)
from software_factory.roles.fake_agent_sdk import ScriptedQuery

if TYPE_CHECKING:
    from pathlib import Path


def commit_messages(remote: Path) -> list[str]:
    log = run_git("log", "--format=%s", f"main..{RUN_BRANCH}", cwd=remote)
    return log.splitlines()[::-1]


def changed_files(review_copy: Path) -> list[str]:
    return run_git("diff", "HEAD", "--name-only", cwd=review_copy).splitlines()


def test_run_with_an_important_finding_each_round(remote: Path, tmp_path: Path) -> None:
    """FR-15's scenario: the implementer's last answer goes to the PR unreviewed."""
    seen = SeenReviewCopies(tmp_path)
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_turn(
                [
                    finding("important", "The deal skips the last player."),
                    finding("nit", "A name could be clearer."),
                    finding("pre_existing", "The shuffle isn't seeded."),
                ],
                seen,
            ),
            implementer_turn(
                {"RULES.md": "Rules\n"},
                "Deal to every player",
                declined=[("R1-F2", "The name matches the rules' term.")],
            ),
            reviewer_turn([finding("important", "The rules skip a turn.")], seen),
            implementer_turn({"RULES.md": "Better rules\n"}, "Keep every turn"),
        ]
    )
    github = fake_github()

    pull_request = start_run(
        services(github, roles, remote, tmp_path / "home"), rounds=2
    )

    assert not roles.turns
    [opened] = github.pull_requests
    assert pull_request.number == opened.number
    assert (opened.head, opened.title) == (RUN_BRANCH, "Add the tiles")
    assert commit_messages(remote) == [
        "Add the tiles",
        "Deal to every player",
        "Keep every turn",
    ]
    # TR-3, and then TR-4.
    assert [changed_files(copy) for copy in seen.copies] == [
        ["TILES.md"],
        ["RULES.md"],
    ]
    # TR-6 for the quality reviewer, and TD-3 for the implementer.
    assert [options.resume for options in roles.options] == [
        None,
        None,
        IMPLEMENTER_SESSION,
        None,
        IMPLEMENTER_SESSION,
    ]
    implementer_prompts = roles.prompts[0::2]
    reviewer_prompts = roles.prompts[1::2]
    assert implementer_prompts[0] == ISSUE_BODY
    # FR-23.
    assert "R1-F1" in implementer_prompts[1]
    assert "R1-F2" in implementer_prompts[1]
    assert "R1-F3" not in implementer_prompts[1]
    assert "R2-F1, an important finding" in implementer_prompts[2]
    # TR-21 and TR-10.
    assert ISSUE_BODY.strip() in reviewer_prompts[0]
    assert "<earlier_findings>\nNone.\n</earlier_findings>" in reviewer_prompts[0]
    assert "R1-F1, an important finding\n" in reviewer_prompts[1]
    assert "R1-F2, a nit, declined by the implementer" in reviewer_prompts[1]
    assert "matches the rules' term" not in reviewer_prompts[1]
    # TR-20.
    assert (
        "R1-F3, a pre-existing finding, not given to the implementer"
        in reviewer_prompts[1]
    )
    # FR-33.
    assert "factory version `0123456789ab`" in opened.body
    # TD-5 and FR-18.
    assert "Closes #7" in opened.body
    assert "**R1-F2**" in opened.body
    assert "The name matches the rules' term." in opened.body
    # FR-25.
    [comment] = github.comments[opened.id]
    assert "**R1-F3**, a pre-existing finding" in comment
    assert "**R1-F2**" not in comment
    assert board_status(github) == "In review"
    # TR-8.
    assert not any((tmp_path / "home" / "working-copies").rglob("*.md"))


def test_round_with_no_important_finding_is_the_last(
    remote: Path, tmp_path: Path
) -> None:
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_turn([finding("nit", "A name could be clearer.")]),
        ]
    )
    github = fake_github()

    start_run(services(github, roles, remote, tmp_path / "home"))

    assert not roles.turns
    assert commit_messages(remote) == ["Add the tiles"]
    [opened] = github.pull_requests
    [comment] = github.comments[opened.id]
    assert "**R1-F1**, a nit" in comment


def test_answer_that_changes_nothing_ends_the_rounds(
    remote: Path, tmp_path: Path
) -> None:
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_turn([finding("important", "The deal skips the last player.")]),
            implementer_turn(
                {},
                "Nothing to commit",
                declined=[("R1-F1", "Every player gets tiles.")],
            ),
        ]
    )
    github = fake_github()

    start_run(services(github, roles, remote, tmp_path / "home"))

    assert not roles.turns
    assert commit_messages(remote) == ["Add the tiles"]
    [opened] = github.pull_requests
    assert "Every player gets tiles." in opened.body


def test_runs_the_rounds_and_turn_caps_the_project_sets(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    push_settings(
        author,
        "rounds = 1\n\n[turn_caps]\nimplementer = 7\nquality_reviewer = 9\n",
    )
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_turn([finding("important", "The deal skips the last player.")]),
            implementer_turn({"TILES.md": "Dealt tiles\n"}, "Deal to every player"),
        ]
    )

    start_run(services(fake_github(), roles, remote, tmp_path / "home"))

    assert not roles.turns
    # FR-6.
    assert [options.max_turns for options in roles.options] == [7, 9, 7]


def test_rounds_the_command_sets_win_over_the_project(
    remote: Path, author: Path, tmp_path: Path
) -> None:
    push_settings(author, "rounds = 1\n")
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            reviewer_turn([finding("important", "The deal skips the last player.")]),
            implementer_turn({"TILES.md": "Dealt tiles\n"}, "Deal to every player"),
            reviewer_turn([]),
        ]
    )

    start_run(services(fake_github(), roles, remote, tmp_path / "home"), rounds=2)

    assert not roles.turns


def test_project_with_no_settings_gets_2_rounds(remote: Path, tmp_path: Path) -> None:
    important = [finding("important", "The deal skips the last player.")]
    roles = ScriptedQuery(
        [
            implementer_turn({"TILES.md": "Tiles\n"}, "Add the tiles"),
            *(
                turn
                for answer in range(2)
                for turn in (
                    reviewer_turn(important),
                    implementer_turn({"TILES.md": f"Tiles {answer}\n"}, "Fix it"),
                )
            ),
        ]
    )

    start_run(services(fake_github(), roles, remote, tmp_path / "home"))

    # FR-32.
    assert not roles.turns
    assert len(commit_messages(remote)) == 3
