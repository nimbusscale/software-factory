from software_factory.config import Settings, TurnCaps
from software_factory.loop.settings import run_settings

DEFAULTS = Settings(rounds=3, turn_caps=TurnCaps(implementer=100, quality_reviewer=100))


def test_project_with_no_settings_file_gets_the_defaults() -> None:
    assert run_settings(None, None) == DEFAULTS


def test_setting_the_project_leaves_out_keeps_its_default() -> None:
    settings = run_settings("[turn_caps]\nimplementer = 40\n", None)

    assert settings == Settings(
        rounds=3, turn_caps=TurnCaps(implementer=40, quality_reviewer=100)
    )


def test_rounds_from_the_command_win_over_the_project() -> None:
    assert run_settings("rounds = 1\n", 5).rounds == 5
