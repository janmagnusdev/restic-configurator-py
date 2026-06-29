import shutil

import click
from pydantic_settings import BaseSettings
from rich.traceback import install

from restic_configurator_py.cli.click_extensions import LazyGroup
from restic_configurator_py.rcy_logging import setup_logging, add_log_file_handler
from restic_configurator_py.rcy_system_configuration import SystemConfiguration


class CliSettings(
    BaseSettings,
    frozen=True,
):
    pass

    @staticmethod
    def bootstrap_cli():
        install(width=shutil.get_terminal_size().columns)
        setup_logging()

    @staticmethod
    def bootstrap_cli_with_system_config(system_config: SystemConfiguration):
        log_file = system_config.get_log_file()
        log_file.parent.mkdir(exist_ok=True, parents=True)
        add_log_file_handler(log_file)


@click.group(name="rcy", cls=LazyGroup)
def cli():
    pass


def main() -> int:
    CliSettings.bootstrap_cli()
    cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
