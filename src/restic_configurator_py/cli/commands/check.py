import click

from restic_configurator_py.cli.cli import cli
from restic_configurator_py.restic_operations.restic_check import restic_check


@cli.command()
@click.pass_context
def cli(ctx: click.Context):
    system = ctx.obj
    restic_check(system)
