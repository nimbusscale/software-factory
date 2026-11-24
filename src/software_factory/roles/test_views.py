import pytest

from software_factory.roles.views import VIEWS_FOLDER, role_views


@pytest.mark.parametrize("file_name", list(role_views()))
def test_view_file_matches_the_code(file_name: str) -> None:
    saved = (VIEWS_FOLDER / file_name).read_text(encoding="utf-8")

    assert saved == role_views()[file_name], (
        f"{file_name} doesn't match the code. Run `uv run write-role-views`."
    )
