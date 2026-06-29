import pytest
from unittest.mock import patch
from click.testing import CliRunner
from restic_configurator_py.cli.cli import cli
from constants import PROJECT_ROOT


@pytest.fixture
def test_config_path():
    return str(PROJECT_ROOT / "systems/example.config.toml")


def test_version_command(test_config_path):
    runner = CliRunner()
    with patch("restic_configurator_py.cli.commands.version.execute") as mock_execute:
        result = runner.invoke(cli, ["version", test_config_path])
        assert result.exit_code == 0
        mock_execute.assert_called_once()
        args, kwargs = mock_execute.call_args
        cmd = args[0]
        assert "version" in cmd


def test_backup_command(test_config_path):
    runner = CliRunner()
    with patch("restic_configurator_py.cli.commands.backup.execute") as mock_execute:
        result = runner.invoke(cli, ["backup", test_config_path, "--print-only"])
        assert result.exit_code == 0
        mock_execute.assert_called_once()
        args, kwargs = mock_execute.call_args
        cmd = args[0]
        assert "backup" in cmd
        assert "--files-from" in cmd
        assert "--exclude-file" in cmd
        assert "--password-file" in cmd


def test_check_command(test_config_path):
    runner = CliRunner()
    with patch("restic_configurator_py.cli.commands.check.execute") as mock_execute:
        result = runner.invoke(cli, ["check", test_config_path])
        assert result.exit_code == 0
        mock_execute.assert_called_once()
        cmd = mock_execute.call_args[0][0]
        assert "check" in cmd


def test_stats_command(test_config_path):
    runner = CliRunner()
    with patch("restic_configurator_py.cli.commands.stats.execute") as mock_execute:
        result = runner.invoke(cli, ["stats", test_config_path])
        assert result.exit_code == 0
        mock_execute.assert_called_once()
        cmd = mock_execute.call_args[0][0]
        assert "stats" in cmd


def test_ls_command(test_config_path):
    runner = CliRunner()
    with patch("restic_configurator_py.cli.commands.ls.execute") as mock_execute:
        result = runner.invoke(cli, ["ls", test_config_path, "snapshot_id"])
        assert result.exit_code == 0
        mock_execute.assert_called_once()
        cmd = mock_execute.call_args[0][0]
        assert "ls" in cmd
        assert "snapshot_id" in cmd


def test_forget_command(test_config_path):
    runner = CliRunner()
    with patch("restic_configurator_py.cli.commands.forget.execute") as mock_execute:
        # forget defaults to dry-run
        result = runner.invoke(cli, ["forget", test_config_path])
        assert result.exit_code == 0
        mock_execute.assert_called_once()
        cmd = mock_execute.call_args[0][0]
        assert "forget" in cmd
        assert "--dry-run" in cmd


def test_get_password_command(test_config_path):
    runner = CliRunner()
    result = runner.invoke(cli, ["get-password", test_config_path])
    assert result.exit_code == 0
    assert "a very secret password" in result.output
