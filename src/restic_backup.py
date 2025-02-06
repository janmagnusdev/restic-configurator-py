import subprocess
from commons import (
    execute_restic_command,
    load_args_and_config_file,
    get_log_file_absolute,
)
import os
import sys

from constants import MACOS, WINDOWS


def restic_backup(
    restic_path,
    repo,
    pass_file_path,
    files_list_path,
    exclude_patterns_path,
    log_folder,
    environment,
    args_scheduled,
):
    backup_command = [
        restic_path,
        "-vv",
        "-r",
        repo,
        "--password-file",
        pass_file_path,
        "backup",
        "--files-from",
        files_list_path,
        "--exclude-file",
        exclude_patterns_path,
    ]
    log_file_absolute = get_log_file_absolute(
        log_folder=log_folder, args_scheduled=args_scheduled, command_name="backup"
    )
    execute_restic_command(
        backup_command, environment=environment, log_file_absolute=log_file_absolute
    )


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


def restic_check(
    restic_path, repo, pass_file_path, environment, log_folder, args_scheduled
):
    check_command = [
        restic_path,
        "-vv",
        "-r",
        repo,
        "--password-file",
        pass_file_path,
        "check",
        "--read-data-subset=500M",
    ]
    execute_restic_command(
        command=check_command,
        environment=environment,
        log_file_absolute=get_log_file_absolute(
            log_folder=log_folder, args_scheduled=args_scheduled, command_name="check"
        ),
    )


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

    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)
    scheduled = args.scheduled

    restic_backup(
        restic_path=restic_path,
        repo=repo,
        pass_file_path=pass_file_path,
        files_list_path=files_list_path,
        exclude_patterns_path=exclude_patterns_path,
        log_folder=log_folder,
        environment=environment,
        args_scheduled=scheduled,
    )

    if "post_backup" in system_config:
        if system_config["post_backup"]["check"]:
            restic_check(
                restic_path=restic_path,
                repo=repo,
                pass_file_path=pass_file_path,
                environment=environment,
                log_folder=log_folder,
                args_scheduled=scheduled,
            )
        if system_config["post_backup"]["forget_dry"]:
            restic_forget(
                restic_path=restic_path,
                repo=repo,
                pass_file_path=pass_file_path,
                environment=environment,
                log_folder=log_folder,
                dry_run=True,
                args_scheduled=scheduled,
            )
        if system_config["post_backup"]["forget"]:
            restic_forget(
                restic_path=restic_path,
                repo=repo,
                pass_file_path=pass_file_path,
                environment=environment,
                log_folder=log_folder,
                dry_run=False,
                args_scheduled=scheduled,
            )
        if system_config["post_backup"]["shutdown"]:
            if current_sys == MACOS:
                subprocess.Popen(
                    ["osascript -e 'tell app 'System Events' to shut down'"], shell=True
                )
            if current_sys == WINDOWS:
                subprocess.Popen(["shutdown /s"], shell=True)

        # all tasks done
        sys.exit(0)


if __name__ == "__main__":
    main()
