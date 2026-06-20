from typing_extensions import deprecated

from restic_configurator_py.load_args import load_args_and_config_file
from restic_configurator_py.rcy_logging import get_log_file_absolute
from restic_configurator_py.restic_operations.execute import execute_restic_command


@deprecated("TODO: this needs to be replaced")
def main():
    loading_result = load_args_and_config_file()
    (
        log_folder,
        restic_path,
        repo,
        pass_file_path,
        files_list_path,
        exclude_patterns_path,
        environment,
        system_config,
        current_sys,
        args,
    ) = loading_result[
        "log_folder",
        "restic_path",
        "repo",
        "pass_file_path",
        "files_list_path",
        "exclude_patterns_path",
        "environment",
        "system_config",
        "current_sys",
        "args",
    ]

    scheduled = args.scheduled
    restic_forget(
        restic_path=restic_path,
        repo=repo,
        pass_file_path=pass_file_path,
        environment=environment,
        log_folder=log_folder,
        dry_run=False,
        args_scheduled=scheduled,
    )


if __name__ == "__main__":
    main()


@deprecated("TODO: this needs to be replaced")
def restic_forget(
    restic_path,
    repo,
    pass_file_path,
    environment,
    log_folder,
    args_scheduled,
    dry_run=True,
):
    forget_command = [
        restic_path,
        "-vv",
        "-r",
        repo,
        "--password-file",
        pass_file_path,
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
    execute_restic_command(
        command=forget_command,
        environment=environment,
        log_file_absolute=get_log_file_absolute(
            log_folder=log_folder, args_scheduled=args_scheduled, command_name="forget"
        ),
    )
