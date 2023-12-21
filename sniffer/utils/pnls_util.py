import os
import signal
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI

from logger import log_info_async, log_error, log_exception_async
from message_broker.websocket_broker import create_broker, socket_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await log_info_async("Server starting.")
    try:
        await create_broker()
    except redis.exceptions.ConnectionError as e:
        # Shut down server if the PNLS fails to create a broker.
        await log_exception_async(f"Failed to establish connection with Redis server due to an Exception: {str(e)}")
    except Exception as e:
        await log_exception_async(f"An exception occurred during the server start up : {str(e)}")
    finally:
        shutdown()
    yield
    await log_info_async("Server shutting down.")
    await socket_broker.close_sockets()


def shutdown():
    """
    Used to shut down the ASGI server.
    """
    log_error(f"Server shut down forcefully.")
    os.kill(os.getpid(), signal.SIGTERM)
