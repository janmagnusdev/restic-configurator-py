import json
from pathlib import Path

import click
from rich.pretty import pprint

from restic_configurator_py.cli.cli import CliSettings, cli
from restic_configurator_py.constants import PROJECT_ROOT
from restic_configurator_py.rcy_logging import create_logger
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger = create_logger(__name__)


@cli.group()
def dev():
    pass


@dev.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def convert_files_list_to_toml(path: Path):
    lines = path.read_text().splitlines()
    lines = [line for line in lines if line and not line.startswith("#")]
    print(json.dumps(lines))


@dev.command()
def print_example_config():
    _settings = CliSettings()
    logger.debug("Hello World!")
    example_config_s = PROJECT_ROOT / "systems/example.config.toml"
    example_config = SystemConfiguration.from_toml_file(example_config_s)
    pprint(example_config)
