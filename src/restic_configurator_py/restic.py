import os
import subprocess

from restic_configurator_py.cli.rcy_console import restic_console, console, copy2clip
from restic_configurator_py.rcy_logging import (
    create_logger,
    create_restic_logger,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger = create_logger(__name__)


def print_and_copy(cmd: list[str], config: SystemConfiguration):
    cmd_string = " ".join(cmd)
    console.print(cmd_string)
    console.print("Environment:")
    console.print(config.make_environment())
    copy2clip(cmd_string)


def print_and_copy_with_env(cmd: list[str], config: SystemConfiguration):

    env_strings = []
    for name, value in config.make_environment().items():
        env_strings.append(f"{name}={value}")
    env_sep = " \\\n"
    env_string = env_sep.join(env_strings)
    env_string = f"{env_string} {env_sep}"

    cmd_string = " ".join(cmd)
    cmd_string = f"{env_string}{cmd_string}"
    console.print(cmd_string)
    copy2clip(cmd_string)


def execute(command: list[str], config: SystemConfiguration, print_only: bool = False):
    logger.info(f"Logging output to {config.get_log_file().resolve()}")
    config.pepper_with_base_command(command)

    if print_only:
        print_and_copy(command, config)
        return 0

    environment = config.make_environment()
    logger.info(f"command to execute: {' '.join(command)}")
    logger.info(f"environment for execution: {environment}")
    restic_logger = create_restic_logger(__name__)

    environment.update(os.environ)
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
