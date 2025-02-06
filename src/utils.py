import subprocess
import re
import os

from dotenv import find_dotenv, dotenv_values


version_check_type = {"result": bool, "min": str, "version": str}


def abs_norm_path(path: str) -> str:
    return os.path.abspath(os.path.normpath(path))


def abs_path_rel_to_given_path(base: str, relative_path: str) -> str:
    return os.path.abspath(os.path.join(base, os.path.normpath(relative_path)))


def resolve_config_path(system_config, path_key: str, system_config_path: str) -> str:
    paths_json = system_config["paths"]
    if path_key not in paths_json:
        raise RuntimeError(f"{path_key} is not in {system_config_path}")

    path = paths_json[path_key]
    if "root_dir" in system_config:
        root_dir = system_config["root_dir"]
        return abs_path_rel_to_given_path(root_dir, path)
    else:
        # need to get dirname from config file path, otherwise resolving relative path won't work
        config_file_dir = os.path.dirname(system_config_path)
        return abs_path_rel_to_given_path(config_file_dir, path)


def read_envs(env_paths: list[str]) -> dict[str, str | None]:
    # start with first, iterate over remaining
    environment = dotenv_values(find_dotenv(env_paths[0]))
    for env_path in env_paths[1:]:
        append = dotenv_values(find_dotenv(env_path))
        environment.update(append)

    # include restic specific RESTIC_PROGRESS_FPS
    environment["RESTIC_PROGRESS_FPS"] = "0.1"

    # also use existing os environment
    environment.update(os.environ)

    print("Using environment:", environment)
    return environment


def check_restic_version(restic_path) -> version_check_type:
    # Define the command you want to execute
    command = f"{restic_path} version"
    output = subprocess.check_output(command, shell=True)
    output_str = output.decode("utf-8")
    pattern = r"(\d\.[\d\.]+)"
    matches = re.findall(pattern, output_str)
    version_number = matches[0] if matches else None
    if version_number is None:
        raise RuntimeError("Could not find")

    min_version = "0.16.0"
    min_version_parts = list(map(int, min_version.split(".")))
    version_parts = list(map(int, version_number.split(".")))
    for index, version_part in enumerate(version_parts):
        if version_part < min_version_parts[index]:
            return {"result": False, "min": min_version, "version": version_number}
    return {"result": True, "min": min_version, "version": version_number}
