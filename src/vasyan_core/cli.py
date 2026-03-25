import asyncio
import pathlib

from .service import ProtoService


class Cli:
    def __init__(self, service: type[ProtoService]) -> None:
        self._service_class = service

    def run(self, *, config: str, name: str | None = None) -> None:
        config_path = pathlib.Path(config)
        service = self._service_class(config_path, name)
        asyncio.run(service.run())
