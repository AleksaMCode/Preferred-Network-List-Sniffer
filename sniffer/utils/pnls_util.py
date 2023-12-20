import os
import signal
from contextlib import asynccontextmanager

from fastapi import FastAPI

from logger import log_info_async, log_error
from message_broker.websocket_broker import create_broker, socket_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await log_info_async("Server starting.")
    try:
        await create_broker()
    except Exception:
        # Shut down server if the PNLS fails to create a broker.
        shutdown()
    yield
    await log_info_async("Server shutting down.")
    await socket_manager.close_sockets()
