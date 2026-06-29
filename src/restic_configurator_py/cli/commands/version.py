from typing import Iterable

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import execute


def restic_version(system_config: SystemConfiguration, restic_args: Iterable[str]):
    cmd = ["version", *restic_args]
    execute(cmd, system_config)


@with_restic_args
@with_system_config
@click.command()
def cli(system_config: SystemConfiguration, restic_args: tuple[str]):
    restic_version(system_config, restic_args)
