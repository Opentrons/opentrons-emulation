"""Logging client for ConcreteCANServerBuilder."""

from typing import Optional

from ..types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateEnvironmentVariables,
    IntermediatePorts,
    IntermediateVolumes,
)
from .abstract_logging_client import AbstractLoggingClient


class CANServerLoggingClient(AbstractLoggingClient):
    """Concrete implementation of AbstractLoggingClient for CANServerServiceBuilder."""

    HEADER_NAME = "CAN Server"

    def __init__(self, dev: bool) -> None:
        """Create CANServerLoggingClient."""
        super().__init__(self.HEADER_NAME, dev)

    def log_build_args(self, build_args: Optional[IntermediateBuildArgs]) -> None:
        """Logs what build args are being set, if any, and why."""
        if build_args is None:
            output = ['Adding no build args since "can-server-source-type" is "local"']
        else:
            output = [
                'Since "can-server-source-type" is "remote", '
                "adding the following build args:",
                *self._logging_console.convert_dict(build_args),
            ]
        self._logging_console.h2_print("build.args")
        self._logging_console.double_tabbed_print(*output)

    def log_volumes(self, volumes: Optional[IntermediateVolumes]) -> None:
        """Logs what volumes are beings added, if any, and why."""
        if volumes is None:
            output = ['Adding no volumes since "can-server-source-type" is "remote".']
        else:
            tabbed_volumes = [f"\t{volume}" for volume in volumes]
            output = [
                'Since "can-server-source-type" is "remote",'
                "adding the following volumes and bind mounts:",
                *tabbed_volumes,
            ]
        self._logging_console.h2_print("volumes")
        self._logging_console.double_tabbed_print(*output)

    def log_command(self, command: Optional[IntermediateCommand]) -> None:
        """Logs that no command is being added."""
        self._logging_console.h2_print("command")
        self._logging_console.double_tabbed_print("Does not require command field.")

    def log_ports(self, ports: Optional[IntermediatePorts]) -> None:
        """Logs what ports are being set, if any, and why."""
        if ports is None:
            output = ["No ports will be exposed."]
        else:
            tabbed_ports = [f'\t"{port}"' for port in ports]
            output = [
                'Since "can-server-exposed-port" is defined, '
                "adding the following ports",
                *tabbed_ports,
            ]
        self._logging_console.h2_print("ports")
        self._logging_console.double_tabbed_print(*output)

    def log_env_vars(
        self, env_vars: Optional[IntermediateEnvironmentVariables]
    ) -> None:
        """Logs that no environment variables are being added."""
        self._logging_console.h2_print("environment")
        self._logging_console.double_tabbed_print(
            "Does not require environment variables."
        )
