from typing_extensions import deprecated

from restic_configurator_py.rcy_system_configuration import (
    SystemConfiguration,
)
from restic_configurator_py.restic_operations.execute import (
    execute,
)


@deprecated("TODO: this needs to be replaced")
def restic_check(
    config: SystemConfiguration,
):

    with (
        config.tmpfile_with("password") as tmp_pass_file,
    ):
        check_command = [
            config.restic_bin,
            "-vv",
            "-r",
            config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "check",
            "--read-data-subset=500M",
        ]
        execute(check_command, config)
