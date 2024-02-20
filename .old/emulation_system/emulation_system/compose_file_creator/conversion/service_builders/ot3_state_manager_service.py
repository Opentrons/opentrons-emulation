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

from ...images import OT3StateManagerImage
from .abstract_service import AbstractService


class OT3StateManagerService(AbstractService):
    """Concrete implementation of AbstractService for building OT-3 State Manager Service."""

    IMAGE_NAME = "ot3-state-manager"
    CONTAINER_NAME = IMAGE_NAME

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        dev: bool,
    ) -> None:
        """Instantiates a OT3Services object."""
        super().__init__(config_model, dev)
        self._ot3 = self.get_ot3(config_model)

    @property
    def _image(self) -> str:
        return OT3StateManagerImage().image_name

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self.CONTAINER_NAME, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self._image

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        return self._config_model.required_networks

    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Check to see if OT-3 service has established connection to CAN Service."""
        return None

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        return None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return (
            self._monorepo_source.generate_emulator_mount_strings()
            + self._ot3_source.generate_state_manager_mount_strings()
        )

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        return self._ot3.get_ot3_state_manager_bound_port()

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        env_vars: IntermediateEnvironmentVariables = {"OPENTRONS_PROJECT": "ot3"}

        if self._ot3.state_manager_env_vars is not None:
            env_vars.update(self._ot3.state_manager_env_vars)

        return env_vars
