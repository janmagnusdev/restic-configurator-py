import click

from restic_configurator_py.cli.cli import cli
from restic_configurator_py.restic_operations.restic_forget import restic_forget


@cli.command()
@click.pass_context
@click.option("--dry-run/--no-dry-run", default=True)
def cli(ctx: click.Context, dry_run: bool):
    system = ctx.obj
    restic_forget(system, dry_run)
