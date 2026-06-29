import tomllib

import click

from restic_configurator_py.cli.click_extensions import with_system_config
from restic_configurator_py.rcy_system_configuration import SystemConfiguration


@with_system_config
@click.command()
def cli(config: SystemConfiguration) -> None:
    data = tomllib.loads(config.secrets_file.read_text("utf-8"))
    print(data["repo"]["password-cmd"])
