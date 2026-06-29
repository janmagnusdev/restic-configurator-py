import sys

import click

from restic_configurator_py.cli.click_extensions import (
    with_system_config,
    with_restic_args,
)
from restic_configurator_py.restic import print_and_copy, print_and_copy_with_env
from restic_configurator_py.rcy_system_configuration import SystemConfiguration


def restic_stub(
    system_config: SystemConfiguration, restic_args: list[str], cp_env: bool
):
    cmd = [
        "-r",
        system_config.restic_repo_url,
        "--password-command",
        f"'{system_config.get_password_cmd()}'",
        *restic_args,
    ]
    cmd = system_config.pepper_with_base_command(cmd)
    if cp_env:
        print_and_copy_with_env(cmd, system_config)
    else:
        print_and_copy(cmd, system_config)
    return 0


@with_system_config
@with_restic_args
@click.command()
@click.option("--cp-env", default=False, is_flag=True)
def cli(system_config: SystemConfiguration, restic_args: list[str], cp_env: bool):
    sys.exit(restic_stub(system_config, restic_args, cp_env))
