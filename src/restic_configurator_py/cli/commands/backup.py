from typing import Iterable

import click

from restic_configurator_py.cli.lazy_group import with_restic_args, with_print_only
from restic_configurator_py.rcy_logging import create_logger
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.execute import execute
from restic_configurator_py.cli.commands.unlock import restic_unlock

logger = create_logger(__name__)


def restic_backup(
    system_config: SystemConfiguration,
    restic_args: Iterable[str],
    *,
    try_no=0,
    print_only: bool = False,
):

    with (
        system_config.tmpfile_with("include_patterns") as tmp_include_file,
        system_config.tmpfile_with("exclude_patterns") as tmp_exclude_file,
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "backup",
            "--files-from",
            tmp_include_file,
            "--exclude-file",
            tmp_exclude_file,
        ]

        exit_code = execute(cmd, system_config, print_only=print_only)
        if exit_code == 11:
            logger.warning("Repo is already locked - unlocking, then trying 1x again")
            restic_unlock(system_config, [])
            restic_backup(system_config, restic_args, try_no=try_no + 1)
            if try_no >= 1:
                logger.error("Repo is already locked and unlocking did not work.")


@with_restic_args
@with_print_only
@click.command()
@click.pass_context
def cli(ctx: click.Context, restic_args: tuple[str], print_only: bool):
    system_config = ctx.obj
    restic_backup(system_config, restic_args, print_only=print_only)
