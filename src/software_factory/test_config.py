import pytest
from pydantic import ValidationError

from software_factory.config import FactoryConfig, StatusKey

STATUS = {"name": "In review", "color": "BLUE", "description": "Ready."}
SETTINGS = {
    "rounds": 3,
    "turn_caps": {"implementer": 100, "quality_reviewer": 100},
    "check_docs": {"ignore": []},
}


def test_config_without_every_status_is_refused() -> None:
    keys = [key for key in StatusKey.__value__.__args__ if key != "needs_attention"]
    config = {
        "board": {"owner": "nimbusscale", "number": 1},
        "statuses": dict.fromkeys(keys, STATUS),
        "labels": {},
        "settings": SETTINGS,
    }

    with pytest.raises(ValidationError, match=r"no status needs_attention\."):
        FactoryConfig.model_validate(config)
