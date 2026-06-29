import sys
from typing import Iterable

import click

from restic_configurator_py import network
from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.rcy_logging import create_logger
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import execute


def restic_check(
    config: SystemConfiguration,
    restic_args: Iterable[str],
):
    logger = create_logger(__name__)

    with (
        config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "check",
            "--read-data-subset=500M",
            *restic_args,
        ]
        exit_code = execute(cmd, config)

        if exit_code != 0 and config.notify_mail:
            try:
                msg = network.create_message(
                    "Restic check failed. Check your logs!",
                    config.notify_mail,
                    f"Check failed with f{exit_code}",
                )
                network.send(msg)
            except Exception as e:
                logger.exception(
                    "Failed to send notification. Repo might be broken and you could not be notified!",
                    exc_info=e,
                )
                raise e
        return exit_code


@with_restic_args
@with_system_config
@click.command()
def cli(config: SystemConfiguration, restic_args: tuple[str]):
    sys.exit(restic_check(config, restic_args))
