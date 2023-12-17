from loguru import logger

from settings import LOGGING


def create_logger(file_name: str):
    logger.add(
        file_name,
        format=LOGGING["format"],
        rotation=LOGGING["rotation"],
        retention=LOGGING["retention"],
        enqueue=True,
    )


# TODO: Rename methods.
async def log_info_async(message: str):
    logger.info(message)


async def log_error_async(message: str):
    logger.error(message)


async def log_exception_async(message: str):
    logger.exception(message)


async def log_warning_async(message: str):
    logger.warning(message)


def log_info(message: str):
    logger.info(message)


def log_error(message: str):
    logger.error(message)


def log_exception(message: str):
    logger.exception(message)


def log_warning(message: str):
    logger.warning(message)
