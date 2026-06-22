from typing import Literal, Iterable

import click

from restic_configurator_py.cli.lazy_group import with_restic_args
from restic_configurator_py.execute import execute


def restic_repair(system_config, repair_command, restic_args: Iterable[str]):
    with (
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "repair",
            repair_command,
            *restic_args,
        ]

        execute(cmd, system_config)


@with_restic_args
@click.command()
@click.pass_context
@click.argument("repair_command")
def cli(
    ctx: click.Context,
    repair_command: Literal["index", "packs", "snapshots"],
    restic_args: tuple[str],
):
    system = ctx.obj
    if repair_command not in ["index", "packs", "snapshots"]:
        raise RuntimeError(f"Invalid repair command: {repair_command}")
    restic_repair(system, repair_command, restic_args)
