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
from emulation_system.compose_file_creator.utilities.hardware_utils import is_ot3

from ...images import MonorepoBuilderImage
from .abstract_service import AbstractService


class MonorepoBuilderService(AbstractService):
    """Concrete implementation of AbstractService for building monorepo-builder Service."""

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        dev: bool,
    ) -> None:
        """Instantiates a MonorepoBuilderService object."""
        super().__init__(config_model, dev)

    @property
    def _image(self) -> str:
        return MonorepoBuilderImage().image_name

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
        return self._config_model.required_networks

    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Check to see if ot3-firmware and monorepo exist."""
        return IntermediateHealthcheck(
            interval=10,
            retries=6,
            timeout=10,
            command="(cd /opentrons)",
        )

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        build_args: Optional[IntermediateBuildArgs] = None

        if self._monorepo_source.is_remote():
            build_args = self._monorepo_source.generate_build_args()

        return build_args

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return self._monorepo_source.generate_builder_mount_strings()

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        return None

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        env_vars: IntermediateEnvironmentVariables = {}
        if is_ot3(self._config_model.robot):
            env_vars = {
                "OPENTRONS_PROJECT": "ot3",
            }

        return env_vars
