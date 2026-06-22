import os
import subprocess

from restic_configurator_py.cli import rcy_console
from restic_configurator_py.cli.rcy_console import restic_console, console
from restic_configurator_py.rcy_logging import (
    create_logger,
    create_restic_logger,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger = create_logger(__name__)


def fill_command(command: list[str], config: SystemConfiguration):
    command.insert(0, config.restic_bin)

    for i, cp in enumerate(config.common_restic_cli_params()):
        command.insert(1 + i, cp)


def execute(command: list[str], config: SystemConfiguration, print_only: bool = False):
    fill_command(command, config)
    environment = config.make_environment()

    if print_only:
        cmd = " ".join(command)
        console.print(cmd)
        console.print("Environment:")
        console.print(environment)
        rcy_console.copy2clip(cmd)
        console.print("📋 Copied command to clipboard!", style="blue", emoji=True)
        return 0

    environment.update(os.environ)

    logger.info(f"command to execute: {' '.join(command)}")
    restic_logger = create_restic_logger(__name__)

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
        text=True,
        bufsize=1,  # buf by 1 line
    )

    for line in iter(process.stdout.readline, ""):
        line = line.rstrip("\n")
        restic_console.print(
            line, markup=False
        )  # live to stdout - rich always flushes output
        restic_logger.info(line)  # live to logger

    process.stdout.close()
    return process.wait()  # returns exit code
