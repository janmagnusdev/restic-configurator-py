from typing import Iterable

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import execute


def restic_check(
    config: SystemConfiguration,
    restic_args: Iterable[str],
):

    with (
        config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "check",
            "--read-data-subset=500M",
            *restic_args,
        ]
        execute(cmd, config)


@with_restic_args
@with_system_config
@click.command()
def cli(config: SystemConfiguration, restic_args: tuple[str]):
    restic_check(config, restic_args)
