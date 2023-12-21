import os
import signal
from contextlib import asynccontextmanager

from fastapi import FastAPI

from logger import log_info_async, log_error
from message_broker.websocket_broker import socket_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await log_info_async("Server starting.")
    yield
    await log_info_async("Server shutting down.")
    await socket_broker.close_sockets()


def shutdown():
    """
    Used to shut down the ASGI server.
    """
    log_error(f"Server shut down forcefully.")
    os.kill(os.getpid(), signal.SIGTERM)
