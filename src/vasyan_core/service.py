import abc
import asyncio
import pathlib
import signal
import typing

from .config import GenericConfig
from .logger import configure_logger


class ProtoService(abc.ABC, typing.Generic[GenericConfig]):
    __service_name__: str
    __class_config__: type[GenericConfig]

    def __init__(self, config_path: pathlib.Path, service_name: str | None = None) -> None:
        self._service_name = service_name or self.__service_name__
        self._config = self.__class_config__.load(config_path, self._service_name)
        configure_logger(self._config.logger)
        self.__post_init__()

    def __post_init__(self) -> None:
        return

    @abc.abstractmethod
    async def _run_service(self) -> None:
        ...

    @abc.abstractmethod
    def _stop_service(self) -> None:
        ...

    def _bind_stop_signals(self) -> None:
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(signal.SIGINT, self._stop_service)
        loop.add_signal_handler(signal.SIGTERM, self._stop_service)

    async def _prepare_service(self) -> None:
        return

    async def _cleanup_service(self) -> None:
        return

    async def run(self) -> None:
        self._bind_stop_signals()
        await self._prepare_service()
        await self._run_service()
        await self._cleanup_service()
