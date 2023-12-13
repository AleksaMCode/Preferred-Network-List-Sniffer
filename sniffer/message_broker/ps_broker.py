from redis import asyncio as aioredis

from settings import SERVER


class PubSubBroker:
    def __init__(self, host=SERVER["host"], port=SERVER["redis_port"]):
        self.redis_connection = None
        self.redis_host = host
        self.redis_port = port
        self.pubsub = None

    async def _get_redis_connection(self) -> aioredis.Redis:
        """
        Establishes a connection to Redis.
        :return: Redis connection object.
        """
        return aioredis.Redis(
            host=self.redis_host, port=self.redis_port, auto_close_connection_pool=False
        )

    async def connect(self) -> None:
        """
        Connects to the Redis server and initializes the pubsub client.
        """
        self.redis_connection = await self._get_redis_connection()
        self.pubsub = self.redis_connection.pubsub()

    async def publish(self, channel_id: str, message: str) -> None:
        """
        Publishes a message to a specific Redis channel.
        :param channel_id: Channel ID to publish to.
        :param message: Message to be published.
        """
        await self.redis_connection.publish(channel_id, message)

    async def subscribe(self, channel_id: str) -> aioredis.Redis:
        """
        Subscribes to a Redis channel.
        :param channel_id: Channel ID to subscribe to.
        :return: PubSub object for the subscribed channel
        """
        await self.pubsub.subscribe(channel_id)
        return self.pubsub
