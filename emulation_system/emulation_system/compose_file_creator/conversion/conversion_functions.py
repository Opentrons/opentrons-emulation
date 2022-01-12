"""Functions for converting from SystemConfigurationModel to RuntimeComposeFileModel."""
from typing import (
    Any,
    Dict,
    cast,
)

from pydantic import (
    parse_file_as,
    parse_obj_as,
)

from emulation_system.compose_file_creator.conversion.intermediate_types import (
    RequiredNetworks,
)
from emulation_system.compose_file_creator.conversion.service_creator import (
    ServiceCreator,
)
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    Network,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DEFAULT_NETWORK_NAME,
)


class ToComposeFile:
    """Conversion logic for input file -> compose file.

    Created as a class to allow for encapsulation.
    """

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
        services = ServiceCreator.create_services(config_model, required_networks)
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
    model = ToComposeFile.from_file("/tests/test_resources/sample.json")
    print(model.to_yaml())
