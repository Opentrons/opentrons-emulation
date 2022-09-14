"""Logging client for ConcreteEmulatorProxyBuilder."""

from typing import Optional

from emulation_system.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.logging.logging_client import AbstractLoggingClient


class EmulatorProxyLoggingClient(AbstractLoggingClient):
    """Concrete implementation of AbstractLoggingClient for EmulatorProxyServiceBuilder.

    Overrides non-abstract method log_image_name.
    """

    HEADER_NAME = "Emulator Proxy"

    def __init__(self, dev: bool) -> None:
        """Creates EmulatorProxyLoggingClient."""
        super().__init__(self.HEADER_NAME, dev)

    def log_image_name(
        self, image_name: str, source_type: str, param_name: str
    ) -> None:
        """Logs what image is being set to and why.

        Overrides non-abstract parent method.
        """
        self._logging_console.h2_print("image")
        self._logging_console.double_tabbed_print(
            f'Using image name "{image_name}" since emulator proxy always uses '
            f"it's remote firmware image."
        )

    def log_build_args(self, build_args: Optional[IntermediateBuildArgs]) -> None:
        """Logs what build args are being set and why."""
        assert build_args is not None
        output = [
            'Since "emulator-proxy" is always "remote", '
            "adding the following build args:",
            *self._logging_console.convert_dict(build_args),
        ]
        self._logging_console.h2_print("build.args")
        self._logging_console.double_tabbed_print(*output)

    def log_volumes(self, volumes: Optional[IntermediateVolumes]) -> None:
        """Logs that no volumes are being added."""
        assert volumes is None
        output = ['Adding no volumes since "emulator-proxy" is always "remote".']
        self._logging_console.h2_print("volumes")
        self._logging_console.double_tabbed_print(*output)

    def log_command(self, command: Optional[IntermediateCommand]) -> None:
        """Logs that no command is being added."""
        assert command is None
        self._logging_console.h2_print("command")
        self._logging_console.double_tabbed_print("Does not require command field.")

    def log_ports(self, ports: Optional[IntermediatePorts]) -> None:
        """Logs that no ports are being added."""
        assert ports is None
        self._logging_console.h2_print("ports")
        self._logging_console.double_tabbed_print("Does not require ports field.")

    def log_depends_on(self, depends_on: Optional[IntermediateDependsOn]) -> None:
        """Logs that no depends_ons are being added."""
        assert depends_on is None
        self._logging_console.h2_print("depends_on")
        self._logging_console.double_tabbed_print("Does not require depends_on field.")

    def log_env_vars(
        self, env_vars: Optional[IntermediateEnvironmentVariables]
    ) -> None:
        """Logs what environment variables are being added and why."""
        assert env_vars is not None
        output = [
            '"emulator-proxy" always requires env vars. Setting env vars to:',
            *self._logging_console.convert_dict(env_vars),
        ]
        self._logging_console.h2_print("environment")
        self._logging_console.double_tabbed_print(*output)
