import click

from restic_configurator_py.cli.rcy_console import console
from restic_configurator_py.rcy_logging import create_logger

logger = create_logger(__name__)


@click.command()
def cli():
    console.print("Please use rcy forget instead. It also does pruning.", style="red")
