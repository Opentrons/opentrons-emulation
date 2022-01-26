"""Class for creating intermediate type DockerServices."""
from .service_creation.emulator_proxy_creation import create_emulator_proxy_service
from .service_creation.input_service_creation import configure_input_service
from .service_creation.shared_functions import (
    generate_container_name,
)

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    DockerServices,
    RequiredNetworks,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)


def create_services(
    config_model: SystemConfigurationModel, required_networks: RequiredNetworks
) -> DockerServices:
    """Creates all services to be added to compose file."""
    services = {}
    emulator_proxy_name = None

    if config_model.modules_exist:
        emulator_proxy_service = create_emulator_proxy_service(
            config_model, required_networks
        )
        emulator_proxy_name = emulator_proxy_service.container_name
        services[emulator_proxy_name] = emulator_proxy_service

    services.update(
        {
            generate_container_name(
                container.id, config_model
            ): configure_input_service(
                container, emulator_proxy_name, config_model, required_networks
            )
            for container in config_model.containers.values()
        }
    )

    return DockerServices(services)
