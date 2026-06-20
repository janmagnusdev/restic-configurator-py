import tomllib
from pathlib import Path

import click

from restic_configurator_py.cli.cli import cli
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic_operations.restic_ops import restic_ops
from restic_configurator_py.restic_operations.restic_unlock import restic_unlock


@cli.command()
@click.pass_context
def cli(ctx: click.Context) -> None:
    config: SystemConfiguration = ctx.obj
    data = tomllib.loads(config.secrets_file.read_text("utf-8"))
    print(data["repo"]["password"])
