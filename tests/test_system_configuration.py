import pytest
from pydantic import ValidationError

from constants import PROJECT_ROOT
from rcy_system_configuration import SystemConfiguration


def test_can_read_example_config():
    example_config_string = (
        PROJECT_ROOT / "systems/example-system/config.json"
    ).read_text()
    SystemConfiguration.model_validate_json(example_config_string)


def test_can_not_read_invalid_config():
    with pytest.raises(ValidationError):
        example_config_string = (
            PROJECT_ROOT / "tests/data/invalid_config.json"
        ).read_text()
        SystemConfiguration.model_validate_json(example_config_string)
