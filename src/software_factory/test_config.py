import pytest
from pydantic import ValidationError

from software_factory.config import FactoryConfig

STATUS = {"name": "In review", "color": "BLUE", "description": "Ready."}


def test_config_without_every_status_is_refused() -> None:
    statuses = {"in_development": STATUS, "in_review": STATUS}

    with pytest.raises(ValidationError, match="no status needs_attention"):
        FactoryConfig.model_validate({"statuses": statuses})
