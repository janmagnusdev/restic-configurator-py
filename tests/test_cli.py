import subprocess
from pathlib import Path

import pytest

from constants import PROJECT_ROOT


def test_cli_help():
    result = subprocess.run(
        ["uv", "run", "rcy", "--help"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert "Usage:" in result.stdout.decode()
    print(result.stdout.decode())


cmd_folder = PROJECT_ROOT / "src/restic_configurator_py/cli/commands"
test_system_config = PROJECT_ROOT / "systems/example.config.toml"

cmds_to_test = list(cmd_folder.glob("*.py"))


@pytest.mark.parametrize("cmd", cmds_to_test)
def test_command_entry_points(cmd: Path):
    if cmd.name == "__init__.py":
        return

    proc = subprocess.run(
        ["uv", "run", "rcy", test_system_config.resolve(), cmd.stem, "--help"],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert "Error" not in proc.stdout
    assert "usage" in proc.stdout.lower()


# TODO: use local restic repo for testing, pass via fixture
def test_restic_backup():
    pass
