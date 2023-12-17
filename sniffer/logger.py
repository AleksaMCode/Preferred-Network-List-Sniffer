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
async def log_info(message: str):
    logger.info(message)


async def log_error(message: str):
    logger.error(message)


async def log_exception(message: str):
    logger.exception(message)


async def log_warning(message: str):
    logger.warning(message)

def log_info2(message: str):
    logger.info(message)


def log_error2(message: str):
    logger.error(message)


def log_exception2(message: str):
    logger.exception(message)


def log_warning2(message: str):
    logger.warning(message)
