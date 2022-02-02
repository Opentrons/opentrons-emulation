"""Class for creating intermediate type DockerServices."""
from emulation_system.compose_file_creator.conversion.intermediate_types import (
    DockerServices,
    RequiredNetworks,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from .service_creation.emulator_proxy_creation import create_emulator_proxy_service
from .service_creation.input_service_creation import configure_input_service
from .service_creation.ot3_service_creation import create_ot3_services
from .service_creation.shared_functions import (
    generate_container_name,
)
from .service_creation.smoothie_service_creation import create_smoothie_service
from ..input.hardware_models import (
    OT2InputModel,
    OT3InputModel,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


def create_services(
    config_model: SystemConfigurationModel,
    required_networks: RequiredNetworks,
    global_settings: OpentronsEmulationConfiguration,
) -> DockerServices:
    """Creates all services to be added to compose file."""
    services = {}
    smoothie_name = None

    emulator_proxy_service = create_emulator_proxy_service(
        config_model, required_networks, global_settings
    )
    emulator_proxy_name = emulator_proxy_service.container_name
    assert emulator_proxy_name is not None  # For mypy
    services[emulator_proxy_name] = emulator_proxy_service

    if config_model.robot is not None and config_model.robot.__class__ == OT2InputModel:
        smoothie_service = create_smoothie_service(
            config_model, required_networks, global_settings
        )
        smoothie_name = smoothie_service.container_name
        assert smoothie_name is not None
        services[smoothie_name] = smoothie_service

    if config_model.robot is not None and config_model.robot.__class__ == OT3InputModel:
        ot3_services = create_ot3_services(
            config_model, required_networks, global_settings
        )
        services.update(
            {
                ot3_service.container_name: ot3_service
                for ot3_service in ot3_services
            }
        )

    services.update(
        {
            generate_container_name(
                container.id, config_model
            ): configure_input_service(
                container,
                emulator_proxy_name,
                smoothie_name,
                config_model,
                required_networks,
                global_settings,
            )
            for container in config_model.containers.values()
        }
    )

    return DockerServices(services)
