"""Module to build Docker Compose file."""
from __future__ import annotations

from typing import (
    List,
    Union,
    cast,
)

from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Service,
    Volume1,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.custom_types import Containers
from emulation_system.consts import DOCKERFILE_DIR_LOCATION


class ConversionLayer:
    """Convert input file to Docker Compose File.

    Gathers all necessary information to build file.
    """

    def __init__(self, config_model: SystemConfigurationModel) -> None:
        self._config_model = config_model
        self.compose_model = RuntimeComposeFileModel()

        self._set_version()
        self._create_services()

    def _set_version(self) -> None:
        """Sets version on Compose file."""
        self.compose_model.version = self._config_model.compose_file_version

    @staticmethod
    def _configure_service(container: Containers) -> Service:
        """Configure and return an individual service."""
        service = Service()
        service.container_name = container.id
        service.tty = True
        service.image = f"{container.get_image_name()}:latest"
        service.build = BuildItem(
            context=DOCKERFILE_DIR_LOCATION, target=container.get_image_name()
        )

        service.volumes = cast(List[Union[str, Volume1]], container.get_mount_strings())
        return service

    def _create_services(self) -> None:
        """Define services for compose file."""
        self.compose_model.services = {
            container.id: self._configure_service(container)
            for container in self._config_model.containers.values()
        }

    def add_ports(self) -> None:
        """Adds ports to compose file."""
        # It literally might just be exposing robot server port.
        pass

    def add_env_vars(self) -> None:
        """Adds env vars to compose file."""
        pass

    def add_networks(self) -> None:
        """Adds networks to compose file."""
        # If OT-2 add all to singular network

        # If OT-3 add all CAN stuff to CAN network.
        # Add everything else to singular network.
        pass

    def add_service_dependencies(self) -> None:
        """Adds service dependencies to compose file."""
        pass

    def add_build_args(self) -> None:
        """Adds build arguments to compose file."""
        pass
