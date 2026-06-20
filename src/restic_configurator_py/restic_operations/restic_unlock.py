from restic_configurator_py.rcy_system_configuration import (
    SystemConfiguration,
)
from restic_configurator_py.restic_operations.execute import (
    execute,
)


def restic_unlock(system_config: SystemConfiguration):
    with (
        system_config.tmpfile_with("password") as tmp_pass_file,
    ):
        backup_command = [
            system_config.restic_bin,
            "-vv",
            "-r",
            system_config.restic_repo_url,
            "--password-file",
            tmp_pass_file,
            "unlock",
        ]

        execute(backup_command, system_config)
