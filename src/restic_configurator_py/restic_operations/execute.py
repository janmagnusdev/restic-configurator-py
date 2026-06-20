import subprocess
import sys

from typing_extensions import deprecated

from restic_configurator_py.rcy_logging import create_logger

logger = create_logger(__name__)


@deprecated("TODO: this needs to be replaced")
def execute_restic_command(command: list[str], environment, log_file_absolute: str):
    logger.info(f"command to execute: {' '.join(command)}")

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
