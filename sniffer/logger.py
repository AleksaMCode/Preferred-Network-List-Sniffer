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


async def log_info(message: str):
    logger.info(message)


async def log_error(message: str):
    logger.error(message)
