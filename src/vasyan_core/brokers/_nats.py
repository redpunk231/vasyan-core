import nats
from nats.aio.client import Client
from nats.aio.subscription import Subscription

from ..protocols import SubscribeCallback


class BrokerNats:
    def __init__(self) -> None:
        self._connection: Client | None = None
        self._subscribes: list[Subscription] = []

    @property
    def connection(self) -> Client:
        if self._connection is None:
            raise Exception('TODO')
        return self._connection

    async def connect(self) -> None:
        self._connection = await nats.connect()

    async def disconnect(self) -> None:
        for sub in self._subscribes:
            await sub.unsubscribe()
        await self.connection.drain()
        self._connection = None

    async def send(self, subject: str, payload: bytes) -> None:
        await self.connection.publish(
            subject=subject,
            payload=payload
        )

    async def subscribe(self, subject: str, callback: SubscribeCallback) -> None:
        subscribe = await self.connection.subscribe(
            subject=subject,
            cb=callback
        )
        self._subscribes.append(subscribe)
