import click

from restic_configurator_py.cli.cli import cli
from restic_configurator_py.restic_operations import restic_backup


@cli.command()
@click.pass_context
def cli(ctx: click.Context):
    system = ctx.obj
    restic_backup.restic_backup_via_system_config(system)
