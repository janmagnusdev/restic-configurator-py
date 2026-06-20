import os
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

from restic_configurator_py.constants import MACOS, WINDOWS
from restic_configurator_py.load_args import load_args_and_config_file
from restic_configurator_py.rcy_logging import get_log_file_absolute
from restic_configurator_py.rcy_system_configuration import SystemConfiguration
from restic_configurator_py.restic_operations.execute import execute_restic_command
from restic_configurator_py.restic_operations.restic_check import restic_check
from restic_configurator_py.restic_operations.restic_forget import restic_forget


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


def restic_backup_via_system_config(system_config: SystemConfiguration):
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        tmp_passfile_path: Path = tmp_dir / "passfile.txt"
        tmp_passfile_path.write_text(system_config.password.get_secret_value(), "utf-8")

        tmp_files_list: Path = tmp_dir / "files_list.txt"
        tmp_files_list.write_text(
            "\n".join(system_config.paths.include_patterns), "utf-8"
        )

        tmp_exclude_list: Path = tmp_dir / "exclude.txt"
        tmp_exclude_list.write_text(
            "\n".join(system_config.paths.exclude_patterns), "utf-8"
        )

        environment = deepcopy(system_config.envs)

        # include restic specific RESTIC_PROGRESS_FPS
        environment["RESTIC_PROGRESS_FPS"] = "0.1"

        # also use existing os environment
        environment.update(os.environ)

        restic_backup(
            restic_path=system_config.restic_bin,
            repo=system_config.restic_repo_url,
            pass_file_path=str(tmp_passfile_path.resolve()),
            files_list_path=str(tmp_files_list.resolve()),
            exclude_patterns_path=str(tmp_exclude_list.resolve()),
            log_folder=system_config.paths.log_folder,
            environment=environment,
            args_scheduled=False,
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
