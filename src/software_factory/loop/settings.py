import tomllib
from typing import TYPE_CHECKING

from pydantic import ValidationError

from software_factory.config import Settings, factory_config

if TYPE_CHECKING:
    from collections.abc import Mapping

# The project's settings file, at the root of its repo.
SETTINGS_FILE = "software-factory.toml"


class SettingsError(Exception):
    """A setting isn't valid, so the run doesn't start (FR-5, FR-26).

    The message says why, in words for the owner.
    """


def run_settings(settings_file: str | None, command_rounds: int | None) -> Settings:
    """The settings for a run, from the command, else the project, else the factory.

    `settings_file` is the text of the project's settings file, or None when the
    project has none. `command_rounds` is the number of rounds the command sets, or
    None when it sets none (FR-32).
    """
    settings = project_settings(settings_file)
    if command_rounds is None:
        return settings
    if command_rounds < 1:
        message = (
            f"A run needs at least 1 round, and the command sets {command_rounds}."
        )
        raise SettingsError(message)
    return settings.model_copy(update={"rounds": command_rounds})


def project_settings(settings_file: str | None) -> Settings:
    """Meets TR-14 for the project's settings."""
    defaults = factory_config().settings
    if settings_file is None:
        return defaults
    try:
        values = tomllib.loads(settings_file)
    except tomllib.TOMLDecodeError as error:
        message = f"The project's {SETTINGS_FILE} isn't valid TOML: {error}"
        raise SettingsError(message) from error
    try:
        return Settings.model_validate(merged(defaults.model_dump(), values))
    except ValidationError as error:
        problems = "; ".join(
            f"{'.'.join(str(part) for part in problem['loc'])}: {problem['msg']}"
            for problem in error.errors()
        )
        message = f"The project's {SETTINGS_FILE} has a setting that isn't valid. "
        raise SettingsError(message + problems) from error


def merged(
    defaults: Mapping[str, object], values: Mapping[str, object]
) -> dict[str, object]:
    """The defaults, with each value the project sets in place of its default."""
    result = dict(defaults)
    for name, value in values.items():
        default = defaults.get(name)
        if isinstance(default, dict) and isinstance(value, dict):
            result[name] = merged(default, value)
        else:
            result[name] = value
    return result
