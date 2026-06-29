import sys

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import restic_unlock


@with_restic_args
@with_system_config
@click.command()
def cli(system_config: SystemConfiguration, restic_args: tuple[str]):
    sys.exit(restic_unlock(system_config, restic_args))
