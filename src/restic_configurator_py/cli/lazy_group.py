# in lazy_group.py
import importlib
from pathlib import Path

import click

from restic_configurator_py.rcy_logging import create_logger

HERE = Path(__file__).parent

CMD_MOD = "restic_configurator_py.cli.commands.{}.cli"

logger = create_logger(__name__)


class LazyGroup(click.Group):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lazy_subcommands = self._init_subcommands()

    def _init_subcommands(self) -> dict[str, str]:
        cmds = {}
        for file in (HERE / "commands").glob("*.py"):
            if file.name == "__init__.py":
                continue
            cmd_name = file.stem.replace("_", "-")
            cmds[cmd_name] = CMD_MOD.format(cmd_name)
        return cmds

    def list_commands(self, ctx):
        base = super().list_commands(ctx)
        lazy = sorted(self.lazy_subcommands.keys())
        return base + lazy

    def get_command(self, ctx, cmd_name):
        if cmd_name in self.lazy_subcommands:
            cmd = self._lazy_load(cmd_name)
            return cmd
        cmd = super().get_command(ctx, cmd_name)
        return cmd

    def _lazy_load(self, cmd_name):
        # lazily loading a command, first get the module name and attribute name
        import_path = self.lazy_subcommands[cmd_name]
        modname, cmd_object_name = import_path.rsplit(".", 1)
        # do the import
        mod = importlib.import_module(modname)
        # get the Command object from that module
        cmd_object = getattr(mod, cmd_object_name)
        # check the result to make debugging easier
        if not isinstance(cmd_object, click.Command):
            raise ValueError(
                f"Lazy loading of {import_path} failed by returning "
                "a non-command object"
            )
        return cmd_object


def with_restic_args(obj):
    if isinstance(obj, click.Command):
        if not any(p.name == "restic_args" for p in obj.params):
            obj.params.append(
                click.Argument(["restic_args"], nargs=-1, type=click.UNPROCESSED)
            )
        return obj

    return obj


def with_print_only(obj):
    if isinstance(obj, click.Command):
        if not any(p.name == "print_only" for p in obj.params):
            obj.params.append(
                click.Option(
                    ["--print-only"], is_flag=True, flag_value=True, default=False
                )
            )
        return obj

    return obj
