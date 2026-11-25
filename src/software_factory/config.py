import tomllib
from functools import cache
from importlib.resources import files
from typing import Literal, get_args

from pydantic import BaseModel, ConfigDict, field_validator

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


class FactoryConfig(ConfigModel):
    statuses: dict[StatusKey, BoardStatus]

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
