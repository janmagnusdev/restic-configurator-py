import argparse
import json
import logging
import os
import platform

from restic_configurator_py.constants import MACOS, WINDOWS
from restic_configurator_py.deprecated.load_result import LoadResult
from restic_configurator_py.utils import (
    check_restic_version,
    read_env_from_env_file_path,
    resolve_config_path,
)

logger = logging.getLogger(__name__)


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
        logger.info("System Name: ", system_config["name"])

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
    env_file_path = resolve_config_path(
        system_config, "env_file_path", args.system_config
    )

    path = system_config["restic_exe"]
    restic_path = os.path.abspath(os.path.normpath(path))

    # repo
    repo = system_config["restic_repo_url"]

    # read envs
    environment = read_env_from_env_file_path(env_file_path)

    # determine current sys
    current_sys = platform.system()
    logger.info("Running on...", current_sys)

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
