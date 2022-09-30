"""Logging client for ConcreteOT3ServiceBuilder."""

from typing import Optional

from .abstract_logging_client import AbstractLoggingClient
from ..types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediatePorts,
    IntermediateVolumes,
)


class OT3LoggingClient(AbstractLoggingClient):
    """Concrete implementation of AbstractLoggingClient for ConcreteOT3ServiceBuilder."""

    HEADER_NAME = "OT3"

    def __init__(self, ot3_service_name: str, dev: bool) -> None:
        """Creates OT3LoggingClient."""
        super().__init__(ot3_service_name, dev)

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
            output = ['Adding no volumes since "source-type" is "remote".']
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
            '"ot3 services" always requires env vars. Setting env vars to:',
            *self._logging_console.convert_dict(env_vars),
        ]
        self._logging_console.h2_print("environment")
        self._logging_console.double_tabbed_print(*output)
