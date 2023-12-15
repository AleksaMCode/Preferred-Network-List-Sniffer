import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
from starlette import status

from logger import log_error, log_exception, log_info, log_warning
from message_broker.websocket_broker import WebSocketBroker
from settings import CHANNEL_ID

router = APIRouter(prefix="/ws")
socket_manager = WebSocketBroker()


@router.websocket("/pub/{channel_id}")
async def publish(websocket: WebSocket, channel_id: str):
    # Raise Exception if the channel id is incorrect.
    # More details about status code: https://www.rfc-editor.org/rfc/rfc6455.html#section-7.4.1
    if channel_id != CHANNEL_ID:
        asyncio.create_task(
            log_error(
                f"Publisher ({websocket.client.host}:{websocket.client.port}) used channel id `{channel_id}` instead of `{CHANNEL_ID}`"
            )
        )
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)

    await websocket.accept()
    asyncio.create_task(
        log_info(
            f"Publisher ({websocket.client.host}:{websocket.client.port}) established socket connection successfully."
        )
    )

    try:
        while True:
            data = await websocket.receive_text()
            if data:
                _ = await socket_manager.broadcast_to_channel(
                    channel_id, json.dumps(data)
                )
    except WebSocketDisconnect:
        await log_warning(
            f"Publisher ({websocket.client.host}:{websocket.client.port}) disconnected from the channel `{channel_id}`."
        )
    except Exception as e:
        await log_exception(f"Exception occurred: {str(e)}.")


@router.websocket("/sub/{channel_id}")
async def subscribe(websocket: WebSocket, channel_id: str):
    # Raise Exception if the channel id is incorrect.
    # More details about status code: https://www.rfc-editor.org/rfc/rfc6455.html#section-7.4.1
    if channel_id != CHANNEL_ID:
        asyncio.create_task(
            log_error(
                f"Subscriber ({websocket.client.host}:{websocket.client.port}) used channel id `{channel_id}` instead of `{CHANNEL_ID}`"
            )
        )
        raise WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA)

    try:
        await socket_manager.add_user_to_channel(channel_id, websocket)
        asyncio.create_task(
            log_info(
                f"Client ({websocket.client.host}:{websocket.client.port}) subscribed successfully to the channel."
            )
        )
        while True:
            _ = await websocket.receive_json()
    except WebSocketDisconnect:
        await log_warning(
            f"Client ({websocket.client.host}:{websocket.client.port}) disconnected from the channel `{channel_id}`."
        )
    except Exception as e:
        await log_exception(f"Exception occurred: {str(e)}.")
