import tomllib

import click

from restic_configurator_py.rcy_system_configuration import SystemConfiguration


@click.command()
@click.pass_context
def cli(ctx: click.Context) -> None:
    config: SystemConfiguration = ctx.obj
    data = tomllib.loads(config.secrets_file.read_text("utf-8"))
    print(data["repo"]["password"])
