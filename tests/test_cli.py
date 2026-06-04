import pytest
from _pytest.capture import CaptureFixture
from pydantic_settings import CliApp

from restic_configurator_py.cli import ResticConfiguratorPy


def test_cli_help(capsys: CaptureFixture[str]):
    with pytest.raises(SystemExit):
        CliApp.run(ResticConfiguratorPy, cli_args=["--help"])

    stdout = capsys.readouterr().out
    assert "usage:" in stdout


def test_cli(capsys: CaptureFixture[str]):
    CliApp.run(ResticConfiguratorPy, cli_args=[])

    stdout = capsys.readouterr().out
    assert "name='Example'" in stdout
