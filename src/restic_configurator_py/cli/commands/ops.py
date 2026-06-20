import click

from restic_configurator_py.cli.cli import cli
from restic_configurator_py.restic_operations.restic_ops import restic_ops
from restic_configurator_py.restic_operations.restic_unlock import restic_unlock


@cli.command()
@click.pass_context
def cli(ctx: click.Context):
    system = ctx.obj
    restic_ops(system)
