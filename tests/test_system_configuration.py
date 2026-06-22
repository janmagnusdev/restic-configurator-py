import pytest
from pydantic import ValidationError

from constants import PROJECT_ROOT
from restic_configurator_py.rcy_system_configuration import SystemConfiguration


def test_can_read_example_toml_config():
    toml_path = PROJECT_ROOT / "systems/example.config.toml"
    config = SystemConfiguration.from_toml_file(toml_path)
    assert config.name == "Example"
    assert config.restic_bin == "restic"
    assert config.post_backup.shutdown is False


def test_can_not_read_invalid_config():
    with pytest.raises(ValidationError):
        example_config_string = (
            PROJECT_ROOT / "tests/data/invalid_config.json"
        ).read_text()
        SystemConfiguration.model_validate_json(example_config_string)


def test_absolute_log_folder_path():
    config = SystemConfiguration.from_toml_file(
        PROJECT_ROOT / "systems/example.config.toml"
    )
    assert config.paths.log_folder.is_absolute()
    assert config.paths.log_folder == (PROJECT_ROOT / "systems/logs/").resolve()
