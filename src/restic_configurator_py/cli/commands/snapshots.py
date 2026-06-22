from typing import Iterable

import click

from restic_configurator_py.cli.lazy_group import with_restic_args
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.execute import execute


def restic_snapshots(system: SystemConfiguration, restic_args: Iterable[str]):
    with (
        system.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "snapshots",
            *restic_args,
        ]

        execute(cmd, system)


@with_restic_args
@click.command()
@click.pass_context
def cli(ctx: click.Context, restic_args: tuple[str]):
    system = ctx.obj
    restic_snapshots(system, restic_args)
