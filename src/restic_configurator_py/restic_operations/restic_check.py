from typing_extensions import deprecated

from restic_configurator_py.rcy_logging import get_log_file_absolute
from restic_configurator_py.restic_operations.execute import execute_restic_command


@deprecated("TODO: this needs to be replaced")
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
