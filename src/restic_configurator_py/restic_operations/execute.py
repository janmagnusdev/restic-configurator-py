import os
import subprocess

from restic_configurator_py.rcy_logging import (
    LOG_FILE_PATH,
    create_logger,
    create_restic_logger,
)
from restic_configurator_py.rcy_system_configuration import SystemConfiguration

logger = create_logger(__name__)
restic_logger = create_restic_logger(__name__)


def make_environment(config: SystemConfiguration):
    env = os.environ.copy()
    env.update(config.envs)
    env["RESTIC_UPDATE_FPS"] = "0.1"
    return env


def execute(command: list[str], config: SystemConfiguration):
    logger.info(f"command to execute: {' '.join(command)}")
    logger.info(f"logging restic output to stdout and {LOG_FILE_PATH}")

    environment = make_environment(config)

    if command[0] != config.restic_bin:
        raise RuntimeError("invalid command", config.restic_bin)

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
        text=True,
        bufsize=1,  # buf by 1 line
    )

    for line in iter(process.stdout.readline, ""):
        line = line.rstrip("\n")
        print(line, flush=True)  # live to stdout
        restic_logger.info(line)  # live to logger

    process.stdout.close()
    return process.wait()  # returns exit code
