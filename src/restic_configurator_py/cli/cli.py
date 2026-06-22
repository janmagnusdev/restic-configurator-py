from logging import Logger
from pathlib import Path

import click
from pydantic_settings import BaseSettings
from rich.traceback import install

from restic_configurator_py.cli.lazy_group import LazyGroup
from restic_configurator_py.rcy_logging import setup_logging, create_logger
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger: Logger


class CliSettings(
    BaseSettings,
    frozen=True,
):
    pass

    @staticmethod
    def bootstrap_cli(log_file: Path):
        install()
        setup_logging(log_file)
        global logger
        logger = create_logger(__name__)


@click.group(name="rcy", cls=LazyGroup)
@click.argument("system_config_path", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def cli(ctx: click.Context, system_config_path: Path):
    system_configuration = SystemConfiguration.from_toml_file(system_config_path)
    log_file = system_configuration.get_log_file()
    log_file.parent.mkdir(exist_ok=True, parents=True)

    CliSettings.bootstrap_cli(log_file)
    ctx.obj = system_configuration


def main() -> int:
    cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
