from typing import Iterable

import click

from restic_configurator_py.cli.lazy_group import with_restic_args
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.execute import execute


def restic_version(system_config: SystemConfiguration, restic_args: Iterable[str]):
    cmd = ["version", *restic_args]
    execute(cmd, system_config)


@with_restic_args
@click.command()
@click.pass_context
def cli(ctx: click.Context, restic_args: list[str]):
    system = ctx.obj
    restic_version(system, restic_args)
