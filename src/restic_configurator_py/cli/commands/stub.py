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
        f"'rcy get-password {system_config.file_path}'",
        *restic_args,
    ]
    system_config.pepper_with_base_command(cmd)
    if cp_env:
        print_and_copy_with_env(cmd, system_config)
    else:
        print_and_copy(cmd, system_config)


@with_system_config
@with_restic_args
@click.command()
@click.option("--cp-env", default=False, is_flag=True)
def cli(system_config: SystemConfiguration, restic_args: list[str], cp_env: bool):
    restic_stub(system_config, restic_args, cp_env)
