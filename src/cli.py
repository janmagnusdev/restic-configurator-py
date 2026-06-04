from pprint import pformat
from sysconfig import expand_makefile_vars

from pydantic_settings import BaseSettings, CliApp

import rcy_logging
from constants import PROJECT_ROOT
from rcy_system_configuration import SystemConfiguration

logger = rcy_logging.create_logger(__name__)


class ResticConfiguratorPy(
    BaseSettings,
    cli_kebab_case=True,
    cli_implicit_flags=True,
    cli_prog_name="rcy",
    frozen=True,
):
    def cli_cmd(self):
        logger.debug("Hello World!")
        example_config_string = (
            PROJECT_ROOT / "systems/example-system/config.json"
        ).read_text()
        example_config = SystemConfiguration.model_validate_json(example_config_string)
        logger.debug(example_config)
        print(pformat(example_config))


def main() -> int:
    CliApp.run(ResticConfiguratorPy)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
