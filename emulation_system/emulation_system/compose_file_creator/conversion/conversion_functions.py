"""Functions for converting from SystemConfigurationModel to RuntimeComposeFileModel."""
from typing import Any, Dict, cast

from pydantic import parse_obj_as

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    RequiredNetworks,
)
from emulation_system.compose_file_creator.conversion.service_creator import (
    create_services,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import Network
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DEFAULT_NETWORK_NAME,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


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


def _convert(
    config_model: SystemConfigurationModel,
    global_settings: OpentronsEmulationConfiguration,
) -> RuntimeComposeFileModel:
    """Parses SystemConfigurationModel to compose file."""
    required_networks = _get_required_networks(config_model)
    services = create_services(config_model, required_networks, global_settings)
    return RuntimeComposeFileModel(
        version=config_model.compose_file_version,
        services=services.services,
        networks={
            network_name: Network() for network_name in required_networks.networks
        },
    )


def convert_from_obj(
    input_obj: Dict[str, Any], global_settings: OpentronsEmulationConfiguration
) -> RuntimeComposeFileModel:
    """Parse from obj."""
    return _convert(parse_obj_as(SystemConfigurationModel, input_obj), global_settings)
