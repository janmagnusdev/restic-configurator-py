import shlex
import sys

from commons import execute_restic_command, load_args_and_config_file, get_log_file_absolute
import os


def main():
    loading_result = load_args_and_config_file()
    (
        log_folder,
        restic_path,
        repo,
        pass_file_path,
        environment,
        args,
    ) = loading_result[
        "log_folder",
        "restic_path",
        "repo",
        "pass_file_path",
        "environment",
        "args",
    ]

    if not os.path.isdir(log_folder):
        os.mkdir(log_folder)
    if args.command is None:
        raise RuntimeError("--command is required")

    # since restic_path is the first argument, and that is defined, --command usage is safe
    # however, one could manipulate the restic_exe_path :o but this is only for my usage
    ops_command = [
        restic_path,
        *shlex.split(args.command),
        "-vv",
        "-r",
        repo,
        "--password-file",
        pass_file_path,
    ]

    log_file_absolute = get_log_file_absolute(log_folder=log_folder, args_scheduled=args.scheduled,
                                              command_name="ops")

    execute_restic_command(ops_command, environment=environment, log_file_absolute=log_file_absolute)

    # all tasks done
    sys.exit(0)


if __name__ == "__main__":
    main()
