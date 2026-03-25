import asyncio
import dataclasses
import functools
import re
import subprocess
import sys
import time
import typing

from loguru import logger

T = typing.TypeVar('T')


def asynchronous[T, **P](func: typing.Callable[P, T]) -> typing.Callable[P, typing.Awaitable[T]]:
    @functools.wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return await asyncio.to_thread(func, *args, **kwargs)
    return wrapper


@dataclasses.dataclass(frozen=True)
class CommandResult:
    stdout: str = ''
    stderr: str = ''
    return_code: int | None = None

    def __bool__(self) -> bool:
        return self.return_code == 0


def run_command(command: str, wait: bool = True) -> CommandResult:
    proc = subprocess.Popen(
        [command],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
    )
    if not wait:
        return CommandResult()

    stdout, stderr = proc.communicate()
    return CommandResult(
        stdout=stdout.decode().strip(),
        stderr=stderr.decode().strip(),
        return_code=proc.returncode
    )


async def balanced_loop(
    stop_event: asyncio.Event,
    interval: float,
    tick: float = 1.0
) -> typing.AsyncGenerator[float, None]:
    interval = max(interval, 0)
    start_time = last_yield = time.time()
    yield last_yield

    while not stop_event.is_set():
        try:
            time_to_yield = interval - (time.time() - start_time) % interval
        except ZeroDivisionError:
            time_to_yield = 0

        if time_to_yield > tick:
            await asyncio.sleep(tick)
            continue

        await asyncio.sleep(time_to_yield)
        last_yield = time.time()
        yield last_yield


def extract_by_regex(lines: typing.Iterable[str],
                     regex: re.Pattern,
                     *,
                     group: int = 0
                     ) -> typing.Generator[str, None, None]:
    for line in lines:
        if (regex_match := regex.search(line)) is None:
            continue
        yield regex_match.group(group)


def terminate(message: str, exit_code: int = 1) -> typing.NoReturn:
    log_func = logger.info if exit_code == 0 else logger.error
    log_func(message)
    sys.exit(exit_code)
