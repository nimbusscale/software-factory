import pytest
from pydantic import ValidationError

from software_factory.config import FactoryConfig

STATUS = {"name": "In review", "color": "BLUE", "description": "Ready."}
SETTINGS = {
    "rounds": 3,
    "turn_caps": {"implementer": 100, "quality_reviewer": 100},
    "check_docs": {"ignore": []},
}


def test_config_without_every_status_is_refused() -> None:
    statuses = {"in_development": STATUS, "in_review": STATUS}

    with pytest.raises(ValidationError, match="no status needs_attention"):
        FactoryConfig.model_validate({"statuses": statuses, "settings": SETTINGS})
