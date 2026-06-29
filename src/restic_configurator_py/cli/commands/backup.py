import sys
from typing import Iterable

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_print_only,
    with_system_config,
)
from restic_configurator_py.cli.commands.check import restic_check
from restic_configurator_py.cli.commands.forget import restic_forget
from restic_configurator_py.rcy_logging import create_logger
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import execute

logger = create_logger(__name__)


def restic_backup(
    system_config: SystemConfiguration,
    *,
    restic_args: Iterable[str] | None = None,
    print_only: bool = False,
    forget_after: bool = False,
    check_after: bool = False,
):
    if restic_args is None:
        restic_args = []

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
            *restic_args,
        ]

        exit_code = execute(cmd, system_config, print_only=print_only)

    if forget_after or system_config.post_backup.forget:
        restic_forget(system_config, [], dry_run=system_config.post_backup.forget_dry)
    if check_after or system_config.post_backup.check:
        restic_check(system_config, [])

    return exit_code


@with_print_only
@with_restic_args
@with_system_config
@click.command()
@click.option(
    "--forget/--no-forget",
    default=False,
    help="Whether to run restic forget after the backup.",
)
@click.option(
    "--check/--no-check",
    default=False,
    help="Whether to run restic check after the backup.",
)
def cli(
    system_config: SystemConfiguration,
    restic_args: tuple[str],
    print_only: bool,
    forget: bool,
    check: bool,
):
    sys.exit(
        restic_backup(
            system_config,
            restic_args=restic_args,
            print_only=print_only,
            forget_after=forget,
            check_after=check,
        )
    )
