import asyncio
from pathlib import Path

import pytest

from software_factory.config import factory_config
from software_factory.github import board_setup
from software_factory.github.board_settings import SetUpError
from software_factory.github.board_setup import (
    BOARD_FILE,
    read_board_file,
    set_up_board,
)
from software_factory.github.board_views import BoardFile, ViewInFile
from software_factory.github.fake_board_setup import (
    FakeBoardOwner,
    FakeLabel,
    FakeOption,
    FakeRepo,
    FakeSetupBoard,
)

REPO_ROOT = Path(__file__).parents[3]

BOARD_FILE_FOR_TESTS = BoardFile(
    title="Factory",
    views=[
        ViewInFile(
            name="Factory",
            layout="BOARD_LAYOUT",
            filter="label:factory",
            fields=["Title", "Repository", "Labels"],
        ),
        ViewInFile(
            name="All", layout="TABLE_LAYOUT", filter="", fields=["Title", "Status"]
        ),
    ],
)

READS = {"ReadOwnerBoards", "ReadBoard", "ReadBoardSettings"}


def set_up(owner: FakeBoardOwner, *, check: bool = False) -> list[str]:
    return asyncio.run(set_up_board(owner, BOARD_FILE_FOR_TESTS, check=check))


def owner_with_board(*repos: FakeRepo) -> FakeBoardOwner:
    return FakeBoardOwner(boards=[FakeSetupBoard(repos=list(repos))])


def board_matches_the_file_and_config(board: FakeSetupBoard) -> None:
    statuses = factory_config().statuses.values()
    assert [(o.name, o.color, o.description) for o in board.options] == [
        (s.name, s.color, s.description) for s in statuses
    ]
    field_names = {field_id: name for name, field_id in board.fields.items()}
    assert [
        (v.name, v.layout, v.filter, [field_names[i] for i in v.field_ids])
        for v in board.views
    ] == [(v.name, v.layout, v.filter, v.fields) for v in BOARD_FILE_FOR_TESTS.views]


def test_setting_up_creates_a_missing_board_from_the_file_and_config() -> None:
    owner = FakeBoardOwner()

    set_up(owner)

    # TD-14.
    [board] = owner.boards
    assert board.number == factory_config().board.number
    assert board.title == "Factory"
    board_matches_the_file_and_config(board)


def test_setting_up_a_board_that_differs_makes_it_match() -> None:
    owner = owner_with_board()

    lines = set_up(owner)

    # TD-14.
    board_matches_the_file_and_config(owner.board)
    assert "The status 'Todo' isn't in the factory's config." in "\n".join(lines)
    assert "The view 'View 1' isn't in the board file. It gets deleted." in lines


def test_setting_up_again_changes_nothing() -> None:
    owner = owner_with_board(FakeRepo("nimbusscale/dust-law"))
    set_up(owner)
    owner.operations.clear()

    lines = set_up(owner)

    # TD-14.
    assert lines == []
    assert set(owner.operations) <= READS


def test_check_lists_the_differences_and_changes_nothing() -> None:
    owner = owner_with_board(FakeRepo("nimbusscale/dust-law"))

    lines = set_up(owner, check=True)

    # TD-14.
    assert "The board has no status 'Backlog'. It gets added." in lines
    assert "The view 'Factory' is missing. It gets created." in lines
    assert "nimbusscale/dust-law has no label 'task'. It gets created." in lines
    assert set(owner.operations) <= READS
    assert [o.name for o in owner.board.options] == ["Todo", "In Progress", "Done"]


def test_check_of_a_missing_board_says_it_gets_created() -> None:
    owner = FakeBoardOwner()

    lines = set_up(owner, check=True)

    # TD-14.
    number = factory_config().board.number
    assert lines == [
        f"nimbusscale has no board #{number}. A board titled 'Factory' gets created."
    ]
    assert owner.boards == []


def test_new_board_with_another_number_says_to_set_it_in_the_config() -> None:
    owner = FakeBoardOwner(next_number=factory_config().board.number + 1)

    with pytest.raises(SetUpError) as error:
        set_up(owner)

    # TD-14.
    number = factory_config().board.number + 1
    assert f"Set board.number to {number} in the factory's config" in str(error.value)
    assert owner.operations[-1] == "CreateBoard"


def test_board_with_another_title_is_left_as_it_is() -> None:
    owner = FakeBoardOwner(boards=[FakeSetupBoard(title="road-trip-agent")])

    with pytest.raises(SetUpError, match=r"Check board\.number"):
        set_up(owner)

    # TD-14.
    assert owner.operations == ["ReadOwnerBoards"]


def test_statuses_keep_their_ids_so_issues_keep_their_status() -> None:
    done = FakeOption("Done", "GRAY", "")
    owner = FakeBoardOwner(boards=[FakeSetupBoard(options=[done])])

    set_up(owner)

    # TD-14.
    assert next(o for o in owner.board.options if o.name == "Done").id == done.id


def test_statuses_in_another_order_are_put_in_the_configs() -> None:
    statuses = list(factory_config().statuses.values())
    options = [FakeOption(s.name, s.color, s.description) for s in statuses]
    owner = FakeBoardOwner(boards=[FakeSetupBoard(options=options[::-1])])

    lines = set_up(owner)

    # TD-14.
    assert "The board's statuses are in a different order from the config's." in lines
    assert [o.name for o in owner.board.options] == [s.name for s in statuses]


def test_setting_up_deletes_the_pull_request_linked_to_issue_workflow() -> None:
    owner = owner_with_board()

    set_up(owner)

    # FR-29.
    assert "Pull request linked to issue" not in owner.board.workflows.values()
    assert "Pull request merged" in owner.board.workflows.values()


def test_linked_repos_get_the_factorys_labels_in_place_of_githubs() -> None:
    own_label = FakeLabel("priority", "000000", "")
    bug = FakeLabel("bug", "d73a4a", "Something isn't working")
    repo = FakeRepo("nimbusscale/dust-law", labels=[bug, own_label])
    owner = owner_with_board(repo)

    set_up(owner)

    # TD-14.
    wanted = factory_config().labels
    assert {(x.name, x.color, x.description) for x in repo.labels} == {
        *((name, x.color, x.description) for name, x in wanted.items()),
        ("priority", "000000", ""),
    }
    assert next(x for x in repo.labels if x.name == "bug").id == bug.id


def test_view_with_a_field_the_board_lacks_is_refused() -> None:
    view = ViewInFile(name="All", layout="TABLE_LAYOUT", filter="", fields=["Size"])
    board_file = BoardFile(title="Factory", views=[view])
    owner = owner_with_board()

    with pytest.raises(SetUpError, match="fields the board doesn't have: 'Size'"):
        asyncio.run(set_up_board(owner, board_file, check=True))


def test_the_board_file_names_only_fields_a_new_board_has() -> None:
    board_file = read_board_file(REPO_ROOT / BOARD_FILE)
    owner = FakeBoardOwner()

    asyncio.run(set_up_board(owner, board_file, check=False))

    # TD-14.
    assert [view.name for view in owner.board.views] == [
        view.name for view in board_file.views
    ]


def test_check_command_fails_when_the_board_differs(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    owner = owner_with_board()
    monkeypatch.setattr(board_setup, "gh_graphql", owner)
    monkeypatch.setattr("sys.argv", ["set-up-board", "--check"])
    monkeypatch.chdir(REPO_ROOT)

    with pytest.raises(SystemExit) as exit_info:
        board_setup.main()

    # TD-14.
    assert exit_info.value.code == 1
    assert "It gets added." in capsys.readouterr().out
    assert set(owner.operations) <= READS


def test_command_says_when_the_board_matches(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    owner = owner_with_board()
    monkeypatch.setattr(board_setup, "gh_graphql", owner)
    monkeypatch.chdir(REPO_ROOT)
    monkeypatch.setattr("sys.argv", ["set-up-board"])
    board_setup.main()
    capsys.readouterr()
    monkeypatch.setattr("sys.argv", ["set-up-board", "--check"])

    board_setup.main()

    # TD-14.
    assert capsys.readouterr().out == (
        "The board matches the board file and the config.\n"
    )
