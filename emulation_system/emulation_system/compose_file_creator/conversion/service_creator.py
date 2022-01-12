"""Class for creating intermediate type DockerServices."""
from typing import (
    List,
    Optional,
    Union,
    cast,
)

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    DockerServices,
    RequiredNetworks,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.input.hardware_models.modules.module_model import (  # noqa: E501
    ModuleInputModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Service,
    Volume1,
)
from emulation_system.compose_file_creator.settings.custom_types import Containers
from emulation_system.compose_file_creator.settings.images import EmulatorProxyImages
from emulation_system.consts import DOCKERFILE_DIR_LOCATION


class ServiceCreator:
    """Class to create and return services."""

    @staticmethod
    def _generate_container_name(
        container_id: str, config_model: SystemConfigurationModel
    ) -> str:
        """Generates container name based off of system_unique_id value."""
        return (
            f"{config_model.system_unique_id}-{container_id}"
            if config_model.system_unique_id is not None
            else container_id
        )

    @classmethod
    def _configure_service(
        cls,
        container: Containers,
        emulator_proxy_name: Optional[str],
        config_model: SystemConfigurationModel,
        required_networks: RequiredNetworks,
    ) -> Service:
        """Configure and return an individual service."""
        service_image = f"{container.get_image_name()}:latest"
        service_build = BuildItem(
            context=DOCKERFILE_DIR_LOCATION, target=container.get_image_name()
        )
        mount_strings = cast(List[Union[str, Volume1]], container.get_mount_strings())
        service_depends_on = (
            [emulator_proxy_name]
            if emulator_proxy_name is not None
            and issubclass(container.__class__, ModuleInputModel)
            else None
        )
        service_command = (
            emulator_proxy_name
            if emulator_proxy_name is not None
            and issubclass(container.__class__, ModuleInputModel)
            else None
        )
        service = Service(
            container_name=cls._generate_container_name(container.id, config_model),
            image=service_image,
            tty=True,
            build=service_build,
            networks=required_networks.networks,
            volumes=mount_strings if len(mount_strings) > 0 else None,
            depends_on=service_depends_on,
            command=service_command,
        )
        return service

    @classmethod
    def create_services(
        cls, config_model: SystemConfigurationModel, required_networks: RequiredNetworks
    ) -> DockerServices:
        """Creates all services to be added to compose file."""
        services = {}
        emulator_proxy_name = None

        if config_model.modules_exist:
            # Going to just use the remote image for now. If someone ends up needing
            # the local image it can get added later.
            image = EmulatorProxyImages().remote_firmware_image_name
            emulator_proxy_name = cls._generate_container_name(
                "emulator-proxy", config_model
            )
            services[emulator_proxy_name] = Service(
                container_name=emulator_proxy_name,
                image=f"{image}:latest",
                build=BuildItem(context=DOCKERFILE_DIR_LOCATION, target=image),
                tty=True,
                networks=required_networks.networks,
            )

        services.update(
            {
                cls._generate_container_name(
                    container.id, config_model
                ): cls._configure_service(
                    container, emulator_proxy_name, config_model, required_networks
                )
                for container in config_model.containers.values()
            }
        )

        return DockerServices(services)
