"""Module to build Docker Compose file."""
from __future__ import annotations
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)


class ConversionLayer:
    """Convert input file to Docker Compose File.

    Gathers all necessary information to build file.
    """

    def __init__(self, config_model: SystemConfigurationModel) -> None:
        self._config_model = config_model
        self.compose_model = RuntimeComposeFileModel()

        self._set_version()

    def _set_version(self) -> None:
        """Sets version on Compose file."""
        self.compose_model.version = self._config_model.compose_file_version

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

    def add_bind_mounts(self) -> None:
        """Adds bind mounts to compose file."""
        pass
