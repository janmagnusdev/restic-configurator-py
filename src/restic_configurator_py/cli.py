import json
from pathlib import Path
from pprint import pformat

import click
from pydantic_settings import BaseSettings, CliApp

from restic_configurator_py import rcy_logging, restic_backup
from restic_configurator_py.constants import PROJECT_ROOT
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger = rcy_logging.create_logger(__name__)


class CliSettings(
    BaseSettings,
    frozen=True,
):
    pass


@click.group(name="rcy")
def cli():
    pass


@cli.command()
def backup():
    system = SystemConfiguration.from_toml_file(
        PROJECT_ROOT / "systems/not_checked_in/backblaze_mac/cloudflare-mac.config.toml"
    )
    restic_backup.restic_backup_system_config(system)


@cli.command()
def print_example_config():
    _settings = CliSettings()
    logger.debug("Hello World!")
    example_config_s = PROJECT_ROOT / "systems/example.config.toml"
    example_config = SystemConfiguration.from_toml_file(example_config_s)
    print(pformat(example_config))


@cli.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def convert_files_list_to_toml(path: Path):
    lines = path.read_text().splitlines()
    lines = [line for line in lines if line and not line.startswith("#")]
    print(json.dumps(lines))


def main() -> int:
    cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
