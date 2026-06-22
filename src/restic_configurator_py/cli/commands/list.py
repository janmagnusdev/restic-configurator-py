from typing import Iterable

import click

from restic_configurator_py.cli.lazy_group import with_restic_args
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.execute import execute


def restic_list(system_config: SystemConfiguration, restic_args: Iterable[str]):
    with (
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "list",
            *restic_args,
        ]
        execute(cmd, system_config)


@with_restic_args
@click.command(context_settings={"ignore_unknown_options": True})
@click.pass_context
def cli(ctx: click.Context, restic_args: str) -> None:
    system = ctx.obj
    restic_list(system, restic_args)
