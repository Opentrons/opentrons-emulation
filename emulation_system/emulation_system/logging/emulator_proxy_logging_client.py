from typing import Optional

from emulation_system.compose_file_creator.output.compose_file_model import ListOrDict
from emulation_system.intermediate_types import (
    Command,
    DependsOn,
    EnvironmentVariables,
    Ports,
    Volumes,
)
from emulation_system.logging.logging_client import LoggingClient


class EmulatorProxyLoggingClient(LoggingClient):

    HEADER_NAME = "Emulator Proxy"

    def __init__(self, dev: bool):
        super().__init__(self.HEADER_NAME, dev)

    def log_image_name(
        self, image_name: str, source_type: str, param_name: str
    ) -> None:
        self._logging_console.tabbed_header_print("image")
        self._logging_console.double_tabbed_print(
            f'Using image name "{image_name}" since emulator proxy always uses '
            f"it's remote firmware image."
        )

    def log_build(self, build_args: Optional[ListOrDict]) -> None:
        assert build_args is not None
        output = [
            'Since "emulator-proxy" is always "remote", '
            "adding the following build args:",
            *self._logging_console.convert_dict(build_args.dict()["__root__"]),
        ]
        self._logging_console.tabbed_header_print("build.args")
        self._logging_console.double_tabbed_print(*output)

    def log_volumes(self, volumes: Optional[Volumes]) -> None:
        assert volumes is None
        output = ['Adding no volumes since "emulator-proxy" is always "remote".']
        self._logging_console.tabbed_header_print("volumes")
        self._logging_console.double_tabbed_print(*output)

    def log_command(self, command: Optional[Command]) -> None:
        assert command is None
        self._logging_console.tabbed_header_print("command")
        self._logging_console.double_tabbed_print("Does not require command field.")

    def log_ports(self, ports: Optional[Ports]) -> None:
        assert ports is None
        self._logging_console.tabbed_header_print("ports")
        self._logging_console.double_tabbed_print("Does not require ports field.")

    def log_depends_on(self, depends_on: Optional[DependsOn]) -> None:
        assert depends_on is None
        self._logging_console.tabbed_header_print("depends_on")
        self._logging_console.double_tabbed_print("Does not require depends_on field.")

    def log_env_vars(self, env_vars: Optional[EnvironmentVariables]) -> None:
        assert env_vars is not None
        output = [
            '"emulator-proxy" always requires env vars. Setting env vars to:',
            *self._logging_console.convert_dict(env_vars),
        ]
        self._logging_console.tabbed_header_print("environment")
        self._logging_console.double_tabbed_print(*output)
