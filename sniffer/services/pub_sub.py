import asyncio
import json

import redis
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from starlette import status

from logger import (
    log_error_async,
    log_exception_async,
    log_info_async,
    log_warning_async,
)
from message_broker.websocket_broker import socket_broker
from settings import CHANNEL_ID
from utils.pnls_util import shutdown

router = APIRouter(prefix="/ws")


@router.websocket("/pub/{channel_id}")
async def publish(websocket: WebSocket, channel_id: str):
    # Raise Exception if the channel id is incorrect.
    # More details about status code: https://www.rfc-editor.org/rfc/rfc6455.html#section-7.4.1
    if channel_id != CHANNEL_ID:
        asyncio.create_task(
            log_error_async(
                f"Publisher ({websocket.client.host}:{websocket.client.port}) used channel id `{channel_id}` instead of `{CHANNEL_ID}`"
            )
        )
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)

    try:
        await socket_broker.accept()

        await websocket.accept()
        asyncio.create_task(
            log_info_async(
                f"Publisher ({websocket.client.host}:{websocket.client.port}) established socket connection successfully."
            )
        )

        while True:
            data = await websocket.receive_text()
            if data:
                _ = await socket_broker.broadcast_to_channel(
                    channel_id, json.dumps(data)
                )
    except WebSocketDisconnect:
        await log_warning_async(
            f"Publisher ({websocket.client.host}:{websocket.client.port}) disconnected from the channel `{channel_id}`."
        )
    except redis.exceptions.ConnectionError as e:
        await log_exception_async(
            f"Failed to establish connection with Redis server due to an Exception: {str(e)}"
        )
        shutdown()
    except Exception as e:
        await log_exception_async(f"Exception occurred: {str(e)}.")
        shutdown()


@router.websocket("/sub/{channel_id}")
async def subscribe(websocket: WebSocket, channel_id: str):
    # Raise Exception if the channel id is incorrect.
    # More details about status code: https://www.rfc-editor.org/rfc/rfc6455.html#section-7.4.1
    if channel_id != CHANNEL_ID:
        asyncio.create_task(
            log_error_async(
                f"Subscriber ({websocket.client.host}:{websocket.client.port}) used channel id `{channel_id}` instead of `{CHANNEL_ID}`"
            )
        )
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)

    try:
        await socket_broker.accept()

        await websocket.accept()
        asyncio.create_task(
            log_info_async(
                f"Subscriber ({websocket.client.host}:{websocket.client.port}) established socket connection successfully."
            )
        )

        await socket_broker.add_client_to_channel(websocket)

        while True:
            _ = await websocket.receive_json()
    except WebSocketDisconnect:
        await log_warning_async(
            f"Client ({websocket.client.host}:{websocket.client.port}) disconnected from the channel `{channel_id}`."
        )
    except redis.exceptions.ConnectionError as e:
        await log_exception_async(
            f"Failed to establish connection with Redis server due to an Exception: {str(e)}"
        )
        shutdown()
    except Exception as e:
        await log_exception_async(f"Exception occurred: {str(e)}.")
        shutdown()
