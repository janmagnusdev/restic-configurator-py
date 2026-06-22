import logging
import logging.handlers
import os
import sys
from datetime import datetime
from logging import Logger
from pathlib import Path

from rich.logging import RichHandler
from typing_extensions import deprecated


log_formatter = logging.Formatter(
    fmt="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)
timed_rotating_handler: logging.handlers.TimedRotatingFileHandler


def setup_logging(log_file: Path):
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.DEBUG)

    global timed_rotating_handler
    timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, backupCount=100, when="h", interval=6
    )

    timed_rotating_handler.setFormatter(log_formatter)

    root.addHandler(timed_rotating_handler)
    root.addHandler(RichHandler(rich_tracebacks=True))
    root.info(f"Logging output to {log_file}")


def create_logger(name: str) -> Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(log_formatter)

    logger.addHandler(stream_handler)

    return logger


def create_restic_logger(name: str) -> Logger:
    name_appended = f"{name}.restic"

    logger = logging.getLogger(name_appended)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # stop walking up to "module" and root
    logger.addHandler(
        timed_rotating_handler
    )  # reuse the same instance, file logging preserved

    return logger


@deprecated("TODO: this needs to be replaced")
def get_log_file_absolute(log_folder, args_scheduled, command_name):
    partial_scheduled = ".scheduled" if args_scheduled else ""

    current_time = datetime.now().isoformat()
    # Replace colons (which are invalid characters in file names) with underscores
    current_run_log_file = current_time.replace(":", "_")
    current_run_log_file += f".{command_name}{partial_scheduled}.log"

    return os.path.abspath(os.path.join(log_folder, current_run_log_file))
