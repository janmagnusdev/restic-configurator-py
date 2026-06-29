from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from restic_configurator_py.cli.commands.backup import restic_backup
from restic_configurator_py.rcy_system_configuration import SystemConfiguration


@pytest.fixture
def test_system_config() -> SystemConfiguration:
    return SystemConfiguration.from_toml_file(
        Path(__file__).parent / "data" / "test.config.toml"
    )


@pytest.mark.xfail
def test_restic_backup(mocker: MockerFixture, test_system_config):
    mocker.patch("restic_configurator_py.cli.commands.backup.execute")
    restic_backup(test_system_config, forget_after=False, check_after=False)
