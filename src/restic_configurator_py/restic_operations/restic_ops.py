from rich import print as rprint

from restic_configurator_py.rcy_system_configuration import SystemConfiguration


def restic_ops(config: SystemConfiguration):
    ops_command = [
        config.restic_bin,
        "unlock",
        "-vv",
        "-r",
        config.restic_repo_url,
        "--password-command",
        f"'uv run rcy {config.file_path} get-password'",
    ]
    rprint(" ".join(ops_command))
