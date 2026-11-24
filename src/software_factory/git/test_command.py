from typing import TYPE_CHECKING

from software_factory.git.conftest import run_git

if TYPE_CHECKING:
    from pathlib import Path

    import pytest


def test_git_works_in_cwd_when_git_dir_points_elsewhere(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_git("init", "--quiet", str(tmp_path / "other"), cwd=tmp_path)
    run_git("init", "--quiet", str(tmp_path / "repo"), cwd=tmp_path)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "other" / ".git"))

    git_dir = run_git("rev-parse", "--absolute-git-dir", cwd=tmp_path / "repo")

    assert git_dir == str(tmp_path / "repo" / ".git")


def test_git_never_waits_for_a_username(tmp_path: Path) -> None:
    show = "alias.show-prompt=!printenv GIT_TERMINAL_PROMPT"

    assert run_git("-c", show, "show-prompt", cwd=tmp_path) == "0"
