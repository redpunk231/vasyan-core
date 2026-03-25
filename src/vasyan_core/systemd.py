import os
import pathlib

from .utils import CommandResult, run_command


class SystemdWrapperError(Exception):
    pass


class SystemdWrapper:
    def __init__(self, user: bool = True) -> None:
        self._user = user

    def run_command(self, command: str) -> CommandResult:
        systemctl = 'systemctl --user' if self._user else 'systemctl'
        return run_command(f'{systemctl} {command}')

    def _get_units_folder_path(self) -> pathlib.Path:
        if not self._user:
            raise SystemdWrapperError('Global systemd units not support')

        home_path = pathlib.Path(os.environ['HOME'])
        return home_path / '.config/systemd/user'

    def check_exists(self, unit_name: str) -> bool:
        result = self.run_command(f'systemctl --user cat {unit_name} > /dev/null 2>&1')
        return bool(result)

    def daemon_reload(self) -> None:
        if self.run_command('daemon-reload'):
            return
        raise SystemdWrapperError('Unable to reload systemd daemons')

    def start(self, unit_name: str) -> None:
        if self.run_command(f'start {unit_name}'):
            return
        raise SystemdWrapperError(f'Unable to start {unit_name} systemd unit')

    def stop(self, unit_name: str, missing_ok: bool = False) -> None:
        exists = self.check_exists(unit_name)
        if not exists and missing_ok:
            return

        if self.run_command(f'stop {unit_name}'):
            return
        raise SystemdWrapperError(f'Unable to stop {unit_name} systemd unit')

    def enable(self, unit_name: str) -> None:
        if self.run_command(f'enable {unit_name}'):
            return
        raise SystemdWrapperError(f'Unable to enable {unit_name} systemd unit')

    def create(self, unit_name: str, unit_data: str) -> None:
        units_folder_path = self._get_units_folder_path()
        units_folder_path.mkdir(parents=True, exist_ok=True)

        unit_path = units_folder_path.joinpath(unit_name)
        unit_path.write_text(unit_data)
