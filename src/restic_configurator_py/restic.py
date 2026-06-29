import os
import subprocess
from typing import Iterable

from restic_configurator_py import network
from restic_configurator_py.cli.rcy_console import restic_console, console, copy2clip
from restic_configurator_py.rcy_logging import (
    create_logger,
    create_restic_logger,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger = create_logger(__name__)

RESTIC_REPO_LOCKED_EXIT_CODE = 11


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


def execute(
    command: list[str],
    config: SystemConfiguration,
    print_only: bool = False,
    retry_if_locked=False,
):
    logger.info(f"Logging output to {config.get_log_file().resolve()}")

    if not config.is_peppered(command):
        command = config.pepper_with_base_command(command)

    if print_only:
        print_and_copy(command, config)
        return 0

    environment = config.make_environment()
    logger.info(f"command to execute: {' '.join(command)}")
    logger.info(f"environment for execution: {environment}")

    environment.update(os.environ)
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
        text=True,
        bufsize=1,
    )

    restic_logger = create_restic_logger(__name__)
    for line in iter(process.stdout.readline, ""):
        line = line.rstrip("\n")
        restic_console.log(line, markup=False)
        restic_logger.info(line)
    del restic_logger

    process.stdout.close()
    exit_code = process.wait()
    if exit_code == RESTIC_REPO_LOCKED_EXIT_CODE and retry_if_locked:
        restic_unlock(system_config=config)
        return execute(command, config, print_only, False)

    if exit_code != 0 and config.notify_mail:
        msg = network.create_message(
            content=f"Failed to execute command, exit code {exit_code}. See logs of your system for details.",
            to=config.notify_mail,
            subject="Execute failed",
        )
        network.send(msg)
    return exit_code


def restic_unlock(
    system_config: SystemConfiguration, restic_args: Iterable[str] | None = None
):
    restic_args = [] if not restic_args else restic_args

    with (
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "unlock",
            *restic_args,
        ]

        execute(cmd, system_config)
