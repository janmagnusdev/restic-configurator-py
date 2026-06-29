import click

from restic_configurator_py.cli.rcy_console import console


@click.command()
def cli():
    console.print(
        "Honestly, you should probably use directly restic for this. Run rcy stub restore -- --help to generate a stub command.",
        style="red",
    )
