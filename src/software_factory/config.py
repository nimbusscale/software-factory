import tomllib
from functools import cache
from importlib.resources import files
from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict, Field, field_validator

type StatusKey = Literal["in_development", "in_review", "needs_attention"]

# The colors GitHub's API takes for a status on a board.
type StatusColor = Literal[
    "GRAY", "BLUE", "GREEN", "YELLOW", "ORANGE", "RED", "PINK", "PURPLE"
]


class ConfigModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class BoardStatus(ConfigModel):
    name: str
    color: StatusColor
    description: str


class TurnCaps(ConfigModel):
    implementer: int = Field(ge=1)
    quality_reviewer: int = Field(ge=1)


class Settings(ConfigModel):
    """The settings a run uses. A project can set each one in its settings file."""

    # Meets FR-5.
    rounds: int = Field(ge=1)
    turn_caps: TurnCaps


class DocStandardsSource(ConfigModel):
    # As owner/name.
    repo: str
    # The branch a run takes the doc standards from when its command names none (FR-33).
    branch: str


class FactoryConfig(ConfigModel):
    statuses: dict[StatusKey, BoardStatus]
    doc_standards: DocStandardsSource
    # The factory's default for each setting (FR-4, FR-6).
    settings: Settings

    @field_validator("statuses")
    @classmethod
    def has_every_status(
        cls, statuses: dict[StatusKey, BoardStatus]
    ) -> dict[StatusKey, BoardStatus]:
        missing = set(get_args(StatusKey.__value__)) - set(statuses)
        if missing:
            names = ", ".join(sorted(missing))
            message = f"The factory's config has no status {names}."
            raise ValueError(message)
        return statuses


@cache
def factory_config() -> FactoryConfig:
    text = (files("software_factory") / "factory.toml").read_text(encoding="utf-8")
    return FactoryConfig.model_validate(tomllib.loads(text))
