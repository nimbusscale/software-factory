from typing import TYPE_CHECKING

import pytest

from software_factory.roles import views
from software_factory.roles.views import VIEWS_FOLDER, role_views

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize("file_name", list(role_views()))
def test_view_file_matches_the_code(file_name: str) -> None:
    saved = (VIEWS_FOLDER / file_name).read_text(encoding="utf-8")

    assert saved == role_views()[file_name], (
        f"{file_name} doesn't match the code. Run `uv run write-role-views`."
    )


def test_write_role_views_writes_each_view_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(views, "VIEWS_FOLDER", tmp_path)

    views.main()

    written = {
        path.name: path.read_text(encoding="utf-8") for path in tmp_path.iterdir()
    }
    assert written == role_views()
