from typing import Iterable

import click

from restic_configurator_py.cli.click_extensions import (
    with_restic_args,
    with_system_config,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic import execute


def restic_forget(
    config: SystemConfiguration,
    restic_args: Iterable[str],
    dry_run=True,
    keep_policy=True,
    keep_within_policy=False,
):
    keep_policy_lst = [
        "--keep-daily",
        "14",
        "--keep-weekly",
        "10",
        "--keep-monthly",
        "12",
        "--keep-yearly",
        "5",
    ]

    keep_within_policy_lst = [
        "--keep-within-daily",
        "14d",
        "--keep-within-weekly",
        "1m",
        "--keep-within-monthly",
        "1y",
        "--keep-within-yearly",
        "75y",
    ]

    with config.tmpfile_with("password") as pass_tmpfile:
        forget_command = [
            "-r",
            config.restic_repo_url,
            "--password-file",
            pass_tmpfile,
            "forget",
            *(["--prune"] if config.forget_options.prune else []),
            *(keep_policy_lst if keep_policy else []),
            *(keep_within_policy_lst if keep_within_policy else []),
            *restic_args,
        ]
        if dry_run:
            forget_command.append("--dry-run")
        execute(forget_command, config)


@with_restic_args
@with_system_config
@click.command()
@click.option("--dry-run/--no-dry-run", default=True)
@click.option("--keep-policy", default=False, flag_value=True)
@click.option("--keep-within-policy", default=False, flag_value=True)
def cli(
    config: SystemConfiguration,
    restic_args: list[str],
    dry_run: bool,
    keep_policy: bool,
    keep_within_policy: bool,
):
    if keep_policy and keep_within_policy:
        raise RuntimeError(
            "only one of --keep-policy or --keep-within-policy is allowed"
        )
    restic_forget(
        config,
        restic_args,
        dry_run,
        keep_policy,
        keep_within_policy,
    )
