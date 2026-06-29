import logging
import logging.handlers
from logging import Logger
from pathlib import Path

from rich.logging import RichHandler


log_formatter = logging.Formatter(
    fmt="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)
timed_rotating_handler: logging.handlers.TimedRotatingFileHandler


def setup_logging():
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.DEBUG)
    root.addHandler(RichHandler(rich_tracebacks=True))


def add_log_file_handler(log_file: Path):
    root = logging.getLogger()

    global timed_rotating_handler
    timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(
        log_file, backupCount=100, when="h", interval=6
    )

    root.addHandler(timed_rotating_handler)
    timed_rotating_handler.setFormatter(log_formatter)


def create_logger(name: str) -> Logger:

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    return logger


def create_restic_logger(name: str) -> Logger:
    name_appended = f"{name}.restic"

    logger = logging.getLogger(name_appended)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # stop walking up to "module" and root
    global timed_rotating_handler
    if timed_rotating_handler is not None:
        logger.addHandler(
            timed_rotating_handler
        )  # reuse the same instance, file logging preserved

    return logger
