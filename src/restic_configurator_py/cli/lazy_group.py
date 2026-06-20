# in lazy_group.py
import importlib
from pathlib import Path

import click

HERE = Path(__file__).parent

CMD_MOD = "restic_configurator_py.cli.commands.{}.cli"


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
            return self._lazy_load(cmd_name)
        return super().get_command(ctx, cmd_name)

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
