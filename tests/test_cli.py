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

    cmd_name = cmd.stem.replace("_", "-")
    args = ["uv", "run", "rcy", cmd_name]
    if cmd_name not in ["dev", "prune", "restore"]:
        args.append(test_system_config.resolve())
    args.append("--help")

    proc = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert "Error" not in proc.stdout
    assert "usage" in proc.stdout.lower()
