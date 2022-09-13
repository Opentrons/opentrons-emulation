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


class CANServerLoggingClient(LoggingClient):
    def __init__(self, dev: bool):
        super().__init__(dev)

    def log_build(self, build_args: Optional[ListOrDict]) -> None:
        if build_args is None:
            output = ['Adding no build args since "can-server-source-type" is "local"']
        else:
            output = [
                'Since "can-server-source-type" is "remote", '
                "adding the following build args:",
                f"\t{build_args.dict()['__root__']}",
            ]
        self._logging_console.tabbed_header_print("build.args")
        self._logging_console.double_tabbed_print(*output)

    def log_volumes(self, volumes: Optional[Volumes]) -> None:
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

    def log_command(self, command: Optional[Command]) -> None:
        self._logging_console.tabbed_header_print("command")
        self._logging_console.double_tabbed_print("Does not require command field.")

    def log_ports(self, ports: Optional[Ports]) -> None:
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

    def log_depends_on(self, depends_on: Optional[DependsOn]) -> None:
        self._logging_console.tabbed_header_print("depends_on")
        self._logging_console.double_tabbed_print("Does not require depends_on field.")

    def log_env_vars(self, env_vars: Optional[EnvironmentVariables]) -> None:
        self._logging_console.tabbed_header_print("environment")
        self._logging_console.double_tabbed_print(
            "Does not require environment variables."
        )
