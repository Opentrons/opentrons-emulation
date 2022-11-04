"""Logging client for ConcreteInputServiceBuilder."""

from typing import Optional

from ..types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediatePorts,
    IntermediateVolumes,
)
from .abstract_logging_client import AbstractLoggingClient


class InputLoggingClient(AbstractLoggingClient):
    """Concrete implementation of AbstractLoggingClient for ConcreteInputServiceBuilder."""

    HEADER_NAME = "Input"

    def __init__(self, input_service_name: str, dev: bool) -> None:
        """Creates InputLoggingClient."""
        super().__init__(input_service_name, dev)

    def log_build_args(self, build_args: Optional[IntermediateBuildArgs]) -> None:
        """Logs what build args are being set and why."""
        if build_args is None:
            output = ['Adding no build args since "source-type" is "local"']
        else:
            output = [
                'Since "source-type" is "remote", ' "adding the following build args:",
                *self._logging_console.convert_dict(build_args),
            ]
        self._logging_console.h2_print("build.args")
        self._logging_console.double_tabbed_print(*output)

    def log_volumes(self, volumes: Optional[IntermediateVolumes]) -> None:
        """Logs that no volumes are being added."""
        if volumes is None:
            output = ["Adding no volumes."]
        else:
            tabbed_volumes = [f"\t{volume}" for volume in volumes]
            output = [
                "Adding the following volumes and bind mounts:",
                *tabbed_volumes,
            ]
        self._logging_console.h2_print("volumes")
        self._logging_console.double_tabbed_print(*output)

    def log_command(self, command: Optional[IntermediateCommand]) -> None:
        """Logs that no command is being added."""
        output = []
        if command is None:
            output.append("Does not require command field.")
        else:
            output.append(f"Adding the following command: {command}")
        self._logging_console.h2_print("command")
        self._logging_console.double_tabbed_print(*output)

    def log_ports(self, ports: Optional[IntermediatePorts]) -> None:
        """Logs that no ports are being added."""
        if ports is None:
            output = ["No ports will be exposed."]
        else:
            tabbed_ports = [f'\t"{port}"' for port in ports]
            output = [
                'Since "exposed-port" is defined, adding the following ports:',
                *tabbed_ports,
            ]
        self._logging_console.h2_print("ports")
        self._logging_console.double_tabbed_print(*output)

    def log_depends_on(self, depends_on: Optional[IntermediateDependsOn]) -> None:
        """Logs that no depends_ons are being added."""
        if depends_on is None:
            output = ["No depends_on will be added."]
        else:
            tabbed_depends_on = [f'\t"{name}"' for name in depends_on.keys()]
            output = [
                "Adding the following depends_on:",
                *tabbed_depends_on,
            ]
        self._logging_console.h2_print("depends_on")
        self._logging_console.double_tabbed_print(*output)

    def log_env_vars(
        self, env_vars: Optional[IntermediateEnvironmentVariables]
    ) -> None:
        """Logs what environment variables are being added and why."""
        if env_vars is None:
            output = ["No environment required."]
        else:
            output = [
                "Setting env vars to:",
                *self._logging_console.convert_dict(env_vars),
            ]
        self._logging_console.h2_print("environment")
        self._logging_console.double_tabbed_print(*output)
