"""Functions for converting from SystemConfigurationModel to RuntimeComposeFileModel."""
from dataclasses import dataclass
from typing import (
    Any,
    Dict,
    List,
    Union,
    cast,
)

from pydantic import (
    parse_file_as,
    parse_obj_as,
)

from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    ListOfStrings,
    Network,
    Service,
    Volume1,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.custom_types import (
    Containers,
)
from emulation_system.consts import DOCKERFILE_DIR_LOCATION


@dataclass
class RequiredNetworks:
    """Networks that are required to be created by Docker."""

    networks: List[str]


@dataclass
class DockerServices:
    """All services to be created by Docker."""

    services: Dict[str, Service]


@dataclass
class TopLevelNetworks:
    """Top level network definitions to be added to Compose file."""

    networks: Dict[str, None]


class ToComposeFile:
    """Conversion logic for input file -> compose file.

    Created as a class to allow for encapsulation.
    """

    @staticmethod
    def _create_services(
        config_model: SystemConfigurationModel, required_networks: RequiredNetworks
    ) -> DockerServices:
        """Creates all services to be added to compose file."""

        def configure_service(container: Containers) -> Service:
            """Configure and return an individual service."""
            service = Service()
            service.container_name = container.id
            service.tty = True
            service.image = f"{container.get_image_name()}:latest"
            service.build = BuildItem(
                context=DOCKERFILE_DIR_LOCATION, target=container.get_image_name()
            )
            service.networks = cast(ListOfStrings, required_networks.networks)
            mount_strings = container.get_mount_strings()

            if len(mount_strings) > 0:
                service.volumes = cast(List[Union[str, Volume1]], mount_strings)
            return service

        return DockerServices(
            {
                container.id: configure_service(container)
                for container in config_model.containers.values()
            }
        )

    @staticmethod
    def _get_required_networks(
        config_model: SystemConfigurationModel,
    ) -> RequiredNetworks:
        """Get required networks to create for system."""
        # system_network_name will always be a string because a default value is set for
        # it. mypy is not picking up the default value.
        required_networks = [cast(str, config_model.system_network_name)]
        if config_model.requires_can_network:
            required_networks.append(config_model.can_network_name)

        return RequiredNetworks(required_networks)

    @classmethod
    def _convert(
        cls, config_model: SystemConfigurationModel
    ) -> RuntimeComposeFileModel:
        """Parses SystemConfigurationModel to compose file."""
        required_networks = cls._get_required_networks(config_model)
        services = cls._create_services(config_model, required_networks)
        return RuntimeComposeFileModel(
            version=config_model.compose_file_version,
            services=services.services,
            networks={
                network_name: Network() for network_name in required_networks.networks
            },
        )

    @classmethod
    def from_file(cls, input_file_path: str) -> RuntimeComposeFileModel:
        """Parse from file."""
        return cls._convert(parse_file_as(SystemConfigurationModel, input_file_path))

    @classmethod
    def from_obj(cls, input_obj: Dict[str, Any]) -> RuntimeComposeFileModel:
        """Parse from obj."""
        return cls._convert(parse_obj_as(SystemConfigurationModel, input_obj))


if __name__ == "__main__":
    model = ToComposeFile.from_file(
        "/home/derek-maggio/Documents/repos/opentrons-emulation/emulation_system/tests/"
        "test_resources/sample.json"
    )
    print(model.to_yaml())
