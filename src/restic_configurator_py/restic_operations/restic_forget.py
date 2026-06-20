from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic_operations.execute import execute


def restic_forget(
    config: SystemConfiguration,
    dry_run=True,
):
    with config.tmpfile_with("password") as pass_tmpfile:
        forget_command = [
            config.restic_bin,
            "-vv",
            "-r",
            config.restic_repo_url,
            "--password-file",
            pass_tmpfile,
            "forget",
            "--keep-within-daily",
            "14d",
            "--keep-within-weekly",
            "1m",
            "--keep-within-monthly",
            "1y",
            "--keep-within-yearly",
            "75y",
            "--prune",
        ]
        if dry_run:
            forget_command.append("--dry-run")
        execute(forget_command, config)
