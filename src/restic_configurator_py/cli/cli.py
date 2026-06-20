from pathlib import Path

import click
from pydantic_settings import BaseSettings

from restic_configurator_py import rcy_logging
from restic_configurator_py.cli.lazy_group import LazyGroup
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger = rcy_logging.create_logger(__name__)


class CliSettings(
    BaseSettings,
    frozen=True,
):
    pass


@click.group(name="rcy", cls=LazyGroup)
@click.argument("system_config_path", type=click.Path(exists=True, path_type=Path))
@click.pass_context
def cli(ctx: click.Context, system_config_path: Path):
    system = SystemConfiguration.from_toml_file(system_config_path)
    ctx.obj = system


def main() -> int:
    cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
