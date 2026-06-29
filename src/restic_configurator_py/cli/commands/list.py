import sys
from typing import Iterable

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import execute


def restic_list(system_config: SystemConfiguration, restic_args: Iterable[str]):
    with (
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "list",
            *restic_args,
        ]
        return execute(cmd, system_config)


@with_restic_args
@with_system_config
@click.command()
def cli(system_config: SystemConfiguration, restic_args: tuple[str]):
    sys.exit(restic_list(system_config, restic_args))
