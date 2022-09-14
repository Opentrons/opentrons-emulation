"""Contains Abstract Base Class for all logging clients."""

from abc import ABC, abstractmethod
from typing import Optional

from emulation_system.consts import DEV_DOCKERFILE_NAME, DOCKERFILE_NAME
from emulation_system.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.logging.console import logging_console


class AbstractLoggingClient(ABC):
    """Abstract Base Class for all logging clients.

    Defines all possible logging methods for ConcreteServiceBuilder classes to call.
    Each ConcreteServiceBuilder should use its own concrete implementation of
    AbstractLoggingClient.
    """

    def __init__(self, service_builder_name: str, dev: bool) -> None:
        """Base __init__ method.

        Contains any parameters that are common to all concrete implementations of
        AbstractLoggingClient.
        Calls log_header and log_dockerfile since all concrete implementations will need
        to call it.

        :param service_builder_name: The name of the ConcreteServiceBuilder you are using.  # noqa: E501
        :param dev: Whether you are in dev mode.
        """
        self._dev = dev
        self._logging_console = logging_console
        self.log_header(service_builder_name)
        self.log_dockerfile()

    def log_dockerfile(self) -> None:
        """Logs message detailing which dockerfile is being used and why."""
        if self._dev:
            output = [
                f'Since "dev" is "true" setting build.dockerfile to '
                f'"{DEV_DOCKERFILE_NAME}"'
            ]
        else:
            output = [
                f'Since "dev" is "false" setting build.dockerfile to '
                f'"{DOCKERFILE_NAME}"'
            ]
        self._logging_console.h2_print("build.dockerfile")
        self._logging_console.double_tabbed_print(*output)

    def log_header(self, service_being_built: str) -> None:
        """Logs header for ConcreteServiceBuilder."""
        self._logging_console.h1_print(f"Creating Service for {service_being_built}")

    def log_container_name(
        self,
        passed_container_name: str,
        final_container_name: str,
        system_unique_id: Optional[str],
    ) -> None:
        """Logs what container_name is being set to for the Service.

        Also details how container_name was built and why.
        """
        if system_unique_id is None:
            message = [
                '"system-unique-id" is None.',
                f'Setting container_name as passed to: "{passed_container_name}".',
            ]
        else:
            message = [
                f'"system-unique-id" is "{system_unique_id}".',
                f'Prepending it to passed container name: "{passed_container_name}". ',
                f'Setting container name to "{final_container_name}".',
            ]

        self._logging_console.h2_print("container_name")
        self._logging_console.double_tabbed_print(*message)

    def log_image_name(
        self, image_name: str, source_type: str, param_name: str
    ) -> None:
        """Logs what image is being set to and why."""
        self._logging_console.h2_print("image")
        self._logging_console.double_tabbed_print(
            f'Using image name "{image_name}" since "{param_name}" is "{source_type}".'
        )

    def log_networks(self, networks: IntermediateNetworks) -> None:
        """Logs what networks are being added to Service."""
        tabbed_networks = [f'\t"{network}"' for network in networks]
        self._logging_console.h2_print("networks")
        self._logging_console.double_tabbed_print(
            "Adding the following networks:", *tabbed_networks
        )

    def log_tty(self, is_tty: bool) -> None:
        """Logs what tty is being set to."""
        if is_tty:
            val = "true"
        else:
            val = "false"
        self._logging_console.h2_print("tty")
        self._logging_console.double_tabbed_print(f'Setting tty to "{val}".')

    ############################################################################
    # Note that all below abstract logging methods have parallel methods in    #
    # abstract_service_builder.py that optionally return values. Because these #
    # methods will end up having different values defined as well as different #
    # reasons for defining those values, the API is requiring you to override  #
    # the methods with custom logic.                                           #
    ############################################################################

    @abstractmethod
    def log_build_args(self, build_args: Optional[IntermediateBuildArgs]) -> None:
        """Logs what build args are being set, if any, and why."""
        ...

    @abstractmethod
    def log_volumes(self, volumes: Optional[IntermediateVolumes]) -> None:
        """Logs what volumes are beings added, if any, and why."""
        ...

    @abstractmethod
    def log_command(self, command: Optional[IntermediateCommand]) -> None:
        """Logs what command is being set, if it's being set at all, and why."""
        ...

    @abstractmethod
    def log_ports(self, ports: Optional[IntermediatePorts]) -> None:
        """Logs what ports are being set, if any, and why."""
        ...

    @abstractmethod
    def log_depends_on(self, depends_on: Optional[IntermediateDependsOn]) -> None:
        """Logs what depends_on are being set, if any, and why."""
        ...

    @abstractmethod
    def log_env_vars(
        self, env_vars: Optional[IntermediateEnvironmentVariables]
    ) -> None:
        """Logs what environment values are being set, if any, and why."""
        ...
