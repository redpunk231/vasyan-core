import sys

from loguru import logger

from .config import LoggerConfig

logger.remove()


def configure_logger(config: LoggerConfig | None = None) -> None:
    logger_level = config.level if config else 'DEBUG'
    logger.add(
        sys.stdout,
        colorize=True,
        format='<level>{message}</level>',
        level=logger_level
    )
