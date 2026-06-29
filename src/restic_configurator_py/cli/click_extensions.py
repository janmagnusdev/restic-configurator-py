# in lazy_group.py
import functools
import importlib
import inspect
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

        if not isinstance(cmd_object, click.Command):
            cmd_object = click.command(name=cmd_name)(cmd_object)
        else:
            cmd_object.name = cmd_name

        return cmd_object


def with_system_config(obj):
    if not isinstance(obj, click.Command):
        return obj

    if hasattr(obj, "_with_system_config_applied"):
        return obj

    if not any(p.name == "system_config_path" for p in obj.params):
        obj.params.insert(
            0,
            click.Argument(
                ["system_config_path"], type=click.Path(exists=True, path_type=Path)
            ),
        )

    old_callback = obj.callback

    @functools.wraps(old_callback)
    def new_callback(*args, **kwargs):
        system_config_path = kwargs.pop("system_config_path")

        from restic_configurator_py.rcy_system_configuration import SystemConfiguration
        from restic_configurator_py.cli.cli import CliSettings

        system_configuration = SystemConfiguration.from_toml_file(system_config_path)

        CliSettings.bootstrap_cli()
        CliSettings.bootstrap_cli_with_system_config(system_configuration)

        ctx = click.get_current_context()
        ctx.obj = system_configuration

        sig = inspect.signature(old_callback)
        for name in ["system_config", "system", "config"]:
            if name in sig.parameters:
                kwargs[name] = system_configuration
                break

        return old_callback(*args, **kwargs)

    obj.callback = new_callback
    obj._with_system_config_applied = True
    return obj


def with_restic_args(obj):
    if isinstance(obj, click.Command):
        if not any(p.name == "restic_args" for p in obj.params):
            obj.params.append(
                click.Argument(["restic_args"], nargs=-1, type=click.UNPROCESSED)
            )
        return obj

    return click.argument("restic_args", nargs=-1, type=click.UNPROCESSED)(obj)


def with_print_only(obj):
    if isinstance(obj, click.Command):
        if not any(p.name == "print_only" for p in obj.params):
            obj.params.append(
                click.Option(
                    ["--print-only"], is_flag=True, flag_value=True, default=False
                )
            )
        return obj

    return click.option("--print-only", is_flag=True, default=False)(obj)
