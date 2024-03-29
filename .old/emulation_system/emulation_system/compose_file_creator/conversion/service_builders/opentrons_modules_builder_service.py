"""Module containing OT3Services class."""
from typing import Optional

from emulation_system import SystemConfigurationModel
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)

from ...images import OpentronsModulesBuilderImage
from .abstract_service import AbstractService


class OpentronsModulesBuilderService(AbstractService):
    """Concrete implementation of AbstractService for building opentrons-modules-builder Service."""

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        dev: bool,
    ) -> None:
        """Instantiates a OpentronsModulesBuilderService object."""
        super().__init__(config_model, dev)

    @property
    def _image(self) -> str:
        return OpentronsModulesBuilderImage().image_name

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(self._image, system_unique_id)
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self._image

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        return True

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        networks = self._config_model.required_networks
        return networks

    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Check to see if ot3-firmware and monorepo exist."""
        return IntermediateHealthcheck(
            interval=10,
            retries=6,
            timeout=10,
            command="(cd /opentrons-modules)",
        )

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        build_args: Optional[IntermediateBuildArgs] = None

        if self._opentrons_modules_source.is_remote():
            build_args = self._opentrons_modules_source.generate_build_args()

        return build_args

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return self._opentrons_modules_source.generate_builder_mount_strings()

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        return None

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        return None
