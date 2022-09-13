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


class CANServerLoggingClient(AbstractLoggingClient):

    HEADER_NAME = "CAN Server"

    def __init__(self, dev: bool):
        super().__init__(self.HEADER_NAME, dev)

    def log_build_args(self, build_args: Optional[IntermediateBuildArgs]) -> None:
        if build_args is None:
            output = ['Adding no build args since "can-server-source-type" is "local"']
        else:
            output = [
                'Since "can-server-source-type" is "remote", '
                "adding the following build args:",
                *self._logging_console.convert_dict(build_args),
            ]
        self._logging_console.tabbed_header_print("build.args")
        self._logging_console.double_tabbed_print(*output)

    def log_volumes(self, volumes: Optional[IntermediateVolumes]) -> None:
        if volumes is None:
            output = ['Adding no volumes since "can-server-source-type" is "remote".']
        else:
            tabbed_volumes = [f"\t{volume}" for volume in volumes]
            output = [
                'Since "can-server-source-type" is "remote",'
                "adding the following volumes and bind mounts:",
                *tabbed_volumes,
            ]
        self._logging_console.tabbed_header_print("volumes")
        self._logging_console.double_tabbed_print(*output)

    def log_command(self, command: Optional[IntermediateCommand]) -> None:
        self._logging_console.tabbed_header_print("command")
        self._logging_console.double_tabbed_print("Does not require command field.")

    def log_ports(self, ports: Optional[IntermediatePorts]) -> None:
        if ports is None:
            output = ["No ports will be exposed."]
        else:
            tabbed_ports = [f'\t"{port}"' for port in ports]
            output = [
                'Since "can-server-exposed-port" is defined, '
                "adding the following ports",
                *tabbed_ports,
            ]
        self._logging_console.tabbed_header_print("ports")
        self._logging_console.double_tabbed_print(*output)

    def log_depends_on(self, depends_on: Optional[IntermediateDependsOn]) -> None:
        self._logging_console.tabbed_header_print("depends_on")
        self._logging_console.double_tabbed_print("Does not require depends_on field.")

    def log_env_vars(
        self, env_vars: Optional[IntermediateEnvironmentVariables]
    ) -> None:
        self._logging_console.tabbed_header_print("environment")
        self._logging_console.double_tabbed_print(
            "Does not require environment variables."
        )
