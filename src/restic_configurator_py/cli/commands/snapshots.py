from typing import Iterable

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import execute


def restic_snapshots(system: SystemConfiguration, restic_args: Iterable[str]):
    with (
        system.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "snapshots",
            *restic_args,
        ]

        execute(cmd, system)


@with_restic_args
@with_system_config
@click.command()
def cli(system: SystemConfiguration, restic_args: tuple[str]):
    restic_snapshots(system, restic_args)
