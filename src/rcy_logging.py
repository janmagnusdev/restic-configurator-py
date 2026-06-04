import logging
import logging.handlers
import sys
from logging import Logger

from constants import PROJECT_ROOT

LOG_FILE_PATH = PROJECT_ROOT / "logs/rcy-main-log.log"


def create_logger(name: str) -> Logger:

    log_formatter = logging.Formatter(
        fmt="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    )

    for handler in logging.root.handlers:
        handler.setFormatter(log_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_FILE_PATH, backupCount=100, when="h", interval=6
    )
    timed_rotating_handler.setFormatter(log_formatter)

    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(log_formatter)

    logger.addHandler(timed_rotating_handler)
    logger.addHandler(stream_handler)

    return logger
