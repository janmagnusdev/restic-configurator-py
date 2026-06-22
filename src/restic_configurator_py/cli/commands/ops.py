import click

from restic_configurator_py.cli.rcy_console import console, copy2clip
from restic_configurator_py.rcy_system_configuration import SystemConfiguration


def restic_ops(system_config: SystemConfiguration, restic_args: tuple[str]):
    environment = system_config.make_environment()
    cmd = [
        system_config.restic_bin,
        "-vv",
        "-r",
        system_config.restic_repo_url,
        "--password-command",
        f"'uv run rcy {system_config.file_path} get-password'",
        *restic_args,
    ]
    cmd_string = " ".join(cmd)
    console.print(cmd_string)
    console.print("Environment:")
    console.print(environment)
    copy2clip(cmd_string)
    console.print("📋 Copied command to clipboard!", style="blue", emoji=True)


@click.command()
@click.pass_context
@click.argument("restic_args", nargs=-1, type=click.UNPROCESSED)
def cli(ctx: click.Context, restic_args: tuple[str]):
    system = ctx.obj
    restic_ops(system, restic_args)
