from pathlib import Path

import uvicorn
from starlette import status

from settings import LOGGING, SERVER, CHANNEL_ID
from loguru import logger

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, WebSocketException

from message_broker.websocket_broker import WebSocketBroker

# Create logger.
logger.add(
    f"{Path(__file__).stem}.log",
    format=LOGGING["format"],
    rotation=LOGGING["rotation"],
    retention=LOGGING["rotation"],
)

socket_manager = WebSocketBroker()
app = FastAPI()


@app.websocket("/ws/pub/{channel_id}")
async def publisher(websocket: WebSocket, channel_id: str):
    # Raise Exception if the channel id is incorrect.
    if channel_id != CHANNEL_ID:
        raise WebSocketException(code=status.WS_1014_BAD_GATEWAY)

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            if data:
                _ = await socket_manager.broadcast_to_channel(channel_id, data)
    except WebSocketDisconnect:
        logger.warning(f"Web client disconnected from the channel {channel_id}.")
    except Exception as e:
        logger.exception(f"Exception occurred: {str(e)}.")


@app.websocket("/ws/sub/{channel_id}")
async def subscriber(websocket: WebSocket, channel_id: str):
    # Raise Exception if the channel id is incorrect.
    if channel_id != CHANNEL_ID:
        raise WebSocketException(code=status.WS_1014_BAD_GATEWAY)

    try:
        await socket_manager.add_user_to_channel(channel_id, websocket)
        while True:
            data = await websocket.receive_text()
            if data:
                websocket.send()
    except WebSocketDisconnect:
        logger.warning(f"Web client disconnected from the channel {channel_id}.")
    except Exception as e:
        logger.exception(f"Exception occurred: {str(e)}.")


if __name__ == "__main__":
    uvicorn.run(
        f"{Path(__file__).stem}:app",
        host=SERVER["localhost"],
        port=SERVER["port"],
        reload=True,
    )
