from typing import Iterable

import click

from restic_configurator_py.cli.lazy_group import with_restic_args
from restic_configurator_py.rcy_logging import create_logger
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.execute import execute

logger = create_logger(__name__)


def restic_stats(system_config: SystemConfiguration, restic_args: Iterable[str]):
    with (
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        cmd = [
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "stats",
            *restic_args,
        ]
        execute(cmd, system_config)


@with_restic_args
@click.command()
@click.pass_context
def cli(ctx: click.Context, restic_args: tuple[str]):
    system = ctx.obj
    restic_stats(system, restic_args)
