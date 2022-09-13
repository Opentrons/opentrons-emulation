from abc import ABC, abstractmethod
from typing import Optional

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    Command,
    DependsOn,
    EnvironmentVariables,
    Ports,
    RequiredNetworks,
    Volumes,
)
from emulation_system.compose_file_creator.output.compose_file_model import ListOrDict
from emulation_system.logging.console import logging_console


class LoggingClient(ABC):
    def __init__(self) -> None:
        self._logging_console = logging_console

    def log_header(self, service_being_built: str) -> None:
        self._logging_console.header_print(
            f"Creating Service for {service_being_built}"
        )

    def log_container_name(
        self, container_name: str, system_unique_id: Optional[str]
    ) -> None:
        if system_unique_id is None:
            message = (
                '"system-unique-id" is None. \n'
                f'Setting container_name as passed to: "{container_name}".'
            )
        else:
            message = []
            message.append(f'"system-unique-id" is "{system_unique_id}".')
            message.append(f"Prepending it to passed container name. ")
            message.append(f'Setting container name to "{container_name}".')

        self._logging_console.tabbed_header_print("container_name")
        self._logging_console.double_tabbed_print(*message)

    def log_image_name(self, image_name: str, source_type: str) -> None:
        self._logging_console.tabbed_header_print("image")
        self._logging_console.double_tabbed_print(
            f'Using image name "{image_name}" since '
            f'can-server-source-type is "{source_type}".'
        )

    def log_networks(self, networks: RequiredNetworks) -> None:
        tabbed_networks = [f'\t"{network}"' for network in networks]
        self._logging_console.tabbed_header_print("networks")
        self._logging_console.double_tabbed_print(
            "Adding the following networks:", *tabbed_networks
        )

    def log_tty(self, is_tty: bool) -> None:
        if is_tty:
            val = "true"
        else:
            val = "false"
        self._logging_console.tabbed_header_print("tty")
        self._logging_console.double_tabbed_print(f'Setting "tty" to "{val}".')

    ############################################################################
    # Note that all below abstract logging methods have parallel methods in    #
    # abstract_service_builder.py that optionally return values. Because these #
    # methods will end up having different values defined as well as different #
    # reasons for defining those values, the API is requiring you to override  #
    # the methods with custom logic.                                           #
    ############################################################################

    @abstractmethod
    def log_build(self, build_args: Optional[ListOrDict]) -> None:
        ...

    @abstractmethod
    def log_volumes(self, volumes: Optional[Volumes]) -> None:
        ...

    @abstractmethod
    def log_command(self, command: Optional[Command]) -> None:
        ...

    @abstractmethod
    def log_ports(self, ports: Optional[Ports]) -> None:
        ...

    @abstractmethod
    def log_depends_on(self, depends_on: Optional[DependsOn]) -> None:
        ...

    @abstractmethod
    def log_env_vars(self, env_vars: Optional[EnvironmentVariables]) -> None:
        ...
