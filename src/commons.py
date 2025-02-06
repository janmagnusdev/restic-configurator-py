import platform
import subprocess
import argparse
import json
import os
import sys
from dataclasses import dataclass, astuple
from datetime import datetime

from constants import MACOS, WINDOWS
from utils import resolve_config_path, abs_norm_path, read_envs, check_restic_version


@dataclass
class LoadResult:
    pass_file_path: str
    log_folder: str
    restic_path: str
    repo: str
    environment: dict
    files_list_path: str
    exclude_patterns_path: str
    system_config: dict
    current_sys: str
    args: argparse.Namespace

    def __iter__(self):
        return iter(astuple(self))

    def __getitem__(self, keys):
        return iter(getattr(self, k) for k in keys)


def load_args_and_config_file():
    argument_parser = argparse.ArgumentParser(
        description="Device Agnostic Restic Execution Suite (DARES)"
    )
    argument_parser.add_argument(
        "--system_config", type=str, help="System configuration file"
    )
    argument_parser.add_argument("--command", type=str, help="Command to execute")
    argument_parser.add_argument(
        "--scheduled",
        action="store_true",
        help="Whether this run is scheduled or not. Scheduled Tasks should provide this opt-in. Consumed in producing "
        "logs.",
        default=False,
    )
    args = argument_parser.parse_args()

    with open(args.system_config) as file:
        system_config = json.load(file)
        print("System Name: ", system_config["name"])

    # paths
    pass_file_path = resolve_config_path(
        system_config, "pass_file_path", args.system_config
    )
    log_folder = resolve_config_path(system_config, "log_folder", args.system_config)
    files_list_path = resolve_config_path(
        system_config, "files_list_path", args.system_config
    )
    exclude_patterns_path = resolve_config_path(
        system_config, "exclude_patterns_path", args.system_config
    )

    restic_path = abs_norm_path(system_config["restic_exe"])

    # repo
    repo = system_config["restic_repo_url"]

    # read envs
    environment = read_envs(system_config["env_filenames"])

    # determine current sys
    current_sys = platform.system()
    print("Running on...", current_sys)

    # checks
    if current_sys not in [MACOS, WINDOWS]:
        raise RuntimeError("Unsupported system found:", current_sys)
    if not os.path.isfile(restic_path):
        raise RuntimeError(
            "Could not find RESTIC. Specify another location or install to the given path."
        )
    version_result = check_restic_version(restic_path=restic_path)
    if not version_result["result"]:
        raise RuntimeError(
            f"Version {version_result['version']} is lower than required minimum version {version_result['min']}."
        )

    return LoadResult(
        pass_file_path=pass_file_path,
        log_folder=log_folder,
        restic_path=restic_path,
        repo=repo,
        environment=environment,
        files_list_path=files_list_path,
        exclude_patterns_path=exclude_patterns_path,
        system_config=system_config,
        current_sys=current_sys,
        args=args,
    )


def execute_restic_command(command: list[str], environment, log_file_absolute: str):
    print(f"command to execute: {' '.join(command)}")

    # a appends to the file, w (over)writes; b stands for binary
    with open(log_file_absolute, "wb") as buffered_file_writer:
        buffered_file_writer.truncate()
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        # read from stdout until b"" is read, which stops the iter object
        for c in iter(lambda: process.stdout.read(1), b""):
            sys.stdout.buffer.write(c)
            sys.stdout.buffer.flush()
            buffered_file_writer.write(c)
            buffered_file_writer.flush()


def get_log_file_absolute(log_folder, args_scheduled, command_name):
    partial_scheduled = ".scheduled" if args_scheduled else ""

    current_time = datetime.now().isoformat()
    # Replace colons (which are invalid characters in file names) with underscores
    current_run_log_file = current_time.replace(":", "_")
    current_run_log_file += f".{command_name}{partial_scheduled}.log"

    return os.path.abspath(os.path.join(log_folder, current_run_log_file))
