from commons import load_args_and_config_file
from restic_backup import restic_forget


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
