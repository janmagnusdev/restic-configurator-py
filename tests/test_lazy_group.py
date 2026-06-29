import click
from restic_configurator_py.cli.click_extensions import (
    LazyGroup,
    with_restic_args,
    with_print_only,
)


def test_lazy_group_init():
    lg = LazyGroup()
    assert "version" in lg.lazy_subcommands
    assert "backup" in lg.lazy_subcommands


def test_lazy_group_list_commands():
    lg = LazyGroup()
    cmds = lg.list_commands(None)
    assert "version" in cmds
    assert "backup" in cmds


def test_lazy_group_get_command():
    lg = LazyGroup()
    cmd = lg.get_command(None, "version")
    assert isinstance(cmd, click.Command)
    assert cmd.name == "version"
    # Should have system_config_path and restic_args
    param_names = [p.name for p in cmd.params]
    assert "system_config_path" in param_names
    assert "restic_args" in param_names


def test_lazy_group_get_command_dev():
    lg = LazyGroup()
    cmd = lg.get_command(None, "dev")
    assert isinstance(cmd, click.Group)
    # dev should NOT have system_config_path (automatically applied)
    param_names = [p.name for p in cmd.params]
    assert "system_config_path" not in param_names


def test_with_restic_args_decorator():
    @click.command()
    def my_cmd(restic_args):
        pass

    decorated = with_restic_args(my_cmd)
    assert any(p.name == "restic_args" for p in decorated.params)


def test_with_print_only_decorator():
    @click.command()
    def my_cmd(print_only):
        pass

    decorated = with_print_only(my_cmd)
    assert any(p.name == "print_only" for p in decorated.params)
