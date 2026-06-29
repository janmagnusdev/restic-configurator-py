import sys
from typing import Literal, Iterable

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.restic import execute
from restic_configurator_py.rcy_system_configuration import SystemConfiguration


def restic_repair(system_config, repair_command, restic_args: Iterable[str]):
    with (
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "repair",
            repair_command,
            *restic_args,
        ]

        return execute(cmd, system_config)


@with_restic_args
@with_system_config
@click.command()
@click.argument("repair_command")
def cli(
    system_config: SystemConfiguration,
    repair_command: Literal["index", "packs", "snapshots"],
    restic_args: tuple[str],
):
    if repair_command not in ["index", "packs", "snapshots"]:
        raise RuntimeError(f"Invalid repair command: {repair_command}")
    sys.exit(restic_repair(system_config, repair_command, restic_args))
