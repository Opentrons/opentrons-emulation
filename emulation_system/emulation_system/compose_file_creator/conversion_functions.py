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
    Network,
    Service,
    Volume1,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DEFAULT_NETWORK_NAME,
)
from emulation_system.compose_file_creator.settings.custom_types import (
    Containers,
)
from emulation_system.compose_file_creator.settings.images import EmulatorProxyImages
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

        def generate_container_name(
            container_id: str, config_model: SystemConfigurationModel
        ) -> str:
            """Generates container name based off of system_unique_id value."""
            return (
                f"{config_model.system_unique_id}-{container_id}"
                if config_model.system_unique_id is not None
                else container_id
            )

        def configure_service(container: Containers) -> Service:
            """Configure and return an individual service."""
            service_image = f"{container.get_image_name()}:latest"
            service_build = BuildItem(
                context=DOCKERFILE_DIR_LOCATION, target=container.get_image_name()
            )
            mount_strings = cast(
                List[Union[str, Volume1]], container.get_mount_strings()
            )

            service = Service(
                container_name=generate_container_name(container.id, config_model),
                image=service_image,
                tty=True,
                build=service_build,
                networks=required_networks.networks,
                volumes=mount_strings if len(mount_strings) > 0 else None,
            )
            return service

        services = {
            generate_container_name(container.id, config_model): configure_service(
                container
            )
            for container in config_model.containers.values()
        }

        if config_model.modules_exist:
            # Going to just use the remote image for now. If someone ends up needing
            # the local image it can get added later.
            image = EmulatorProxyImages().remote_firmware_image_name
            name = generate_container_name("emulator-proxy", config_model)
            services[name] = Service(
                container_name=name,
                image=f"{image}:latest",
                build=BuildItem(context=DOCKERFILE_DIR_LOCATION, target=image),
                tty=True,
                networks=required_networks.networks,
            )

        return DockerServices(services)

    @staticmethod
    def _get_required_networks(
        config_model: SystemConfigurationModel,
    ) -> RequiredNetworks:
        """Get required networks to create for system."""
        local_network_name = (
            DEFAULT_NETWORK_NAME
            if config_model.system_unique_id is None
            else config_model.system_unique_id
        )

        required_networks = [cast(str, local_network_name)]
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
