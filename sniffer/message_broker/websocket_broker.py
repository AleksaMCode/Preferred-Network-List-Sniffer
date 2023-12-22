import asyncio
import json
import redis
from fastapi import WebSocket
from redis import asyncio as aioredis
from starlette.websockets import WebSocketState
from message_broker.message_broker import MessageBroker
from settings import CHANNEL_ID

class WebSocketBroker:
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.sockets: list[WebSocket] = []
        self.pubsub_client = MessageBroker()

    async def accept(self) -> None:
        """
        Connects to Redis server and establish channel.
        """
        if not self.sockets:
            await self.pubsub_client.connect()
            ps_subscriber = await self.pubsub_client.subscribe(self.channel_id)
            asyncio.create_task(self._pubsub_data_reader(ps_subscriber))

    async def add_client_to_channel(self, websocket: WebSocket) -> None:
        """
        Adds a client's WebSocket connection to a channel.
        :param websocket: WebSocket connection object.
        """
        self.sockets.append(websocket)

    async def broadcast_to_channel(self, channel_id: str, message: str) -> None:
        """
        Broadcasts a message to all connected WebSockets in a channel.
        :param channel_id: Channel ID to publish to.
        :param message: Message to be broadcast.
        """
        if self.sockets:
            await self.pubsub_client.publish(channel_id, message)

    async def _pubsub_data_reader(self, ps_subscriber: aioredis.Redis):
        """
        Reads and broadcasts messages received from Redis PubSub.
        :param ps_subscriber: PubSub object for the subscribed channel.
        """
        while True:
            message = None
            try:
                message = await ps_subscriber.get_message(ignore_subscribe_messages=True)
            except redis.exceptions.ConnectionError:
            # TODO: Add logging.
            # TODO: Replace return handle when Redis is closed when server is running with a better
            #       approach, perhaps a back-off algorithm could be added.
                return
            except Exception as e:
            # TODO: Implement handle of other Exceptions.    
                pass

            if message:
                for socket in self.sockets:
                    data = message["data"].decode("utf-8")
                    await socket.send_json(json.loads(data))

    async def close_sockets(self):
        """
        Closes client sockets.
        """
        for socket in self.sockets:
            if socket.application_state == WebSocketState.CONNECTED and socket.client_state == WebSocketState.CONNECTED:
                await socket.close()


socket_broker = WebSocketBroker(CHANNEL_ID)
