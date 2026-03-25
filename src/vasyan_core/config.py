import pathlib
import typing

import pydantic
import yaml

LoggerLevel = typing.Annotated[
    typing.Literal['TRACE', 'DEBUG', 'INFO', 'SUCCESS', 'WARNING', 'ERROR', 'CRITICAL'],
    pydantic.BeforeValidator(lambda x: x.upper())
]
GenericConfig = typing.TypeVar('GenericConfig', bound='Config')


class LoggerConfig(pydantic.BaseModel):
    level: LoggerLevel = 'INFO'


class Config(pydantic.BaseModel):
    logger: LoggerConfig = pydantic.Field(default_factory=LoggerConfig)

    @classmethod
    def _read_config_file(cls, config_path: pathlib.Path, service_name: str) -> dict:
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
            return data.get(service_name, {})

    @classmethod
    def load(cls, config_path: pathlib.Path, service_name: str) -> typing.Self:
        raw_data = cls._read_config_file(config_path, service_name)
        return cls.model_validate(raw_data)
