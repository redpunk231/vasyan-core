import typing


class BrokerMessage(typing.Protocol):
    subject: str
    data: bytes


SubscribeCallback = typing.Callable[[BrokerMessage], typing.Awaitable[None]]


class Broker(typing.Protocol):
    async def connect(self) -> None: ...

    async def disconnect(self) -> None: ...

    async def send(self, subject: str, payload: bytes) -> None: ...

    async def subscribe(self, subject: str, callback: SubscribeCallback) -> None: ...
