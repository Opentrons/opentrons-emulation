"""Module containing SmoothieService."""
from typing import Optional

from emulation_system import SystemConfigurationModel
from emulation_system.compose_file_creator.images import SmoothieImage
from emulation_system.compose_file_creator.pipette_utils import get_robot_pipettes
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)

from ...input.hardware_models import OT2InputModel
from ...logging import SmoothieLoggingClient
from .abstract_service import AbstractService


class SmoothieService(AbstractService):
    """Concrete implementation of AbstractService for building a Smoothie Service."""

    SMOOTHIE_NAME = "smoothie"
    SMOOTHIE_DEFAULT_PORT = "11000"

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        dev: bool,
    ) -> None:
        """Instantiates a SmoothieService object."""
        super().__init__(config_model, dev)
        self._ot2 = self.get_ot2(config_model)
        self._logging_client = SmoothieLoggingClient(self._dev)
        self._smoothie_image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        return SmoothieImage().image_name

    def generate_container_name(self) -> str:
        """Generates value for container_name parameter."""
        system_unique_id = self._config_model.system_unique_id
        container_name = super()._generate_container_name(
            self.SMOOTHIE_NAME, system_unique_id
        )
        self._logging_client.log_container_name(
            self.SMOOTHIE_NAME, container_name, system_unique_id
        )
        return container_name

    def generate_image(self) -> str:
        """Generates value for image parameter."""
        return self._image

    @property
    def _image(self) -> str:
        return self._smoothie_image

    def is_tty(self) -> bool:
        """Generates value for tty parameter."""
        tty = True
        self._logging_client.log_tty(tty)
        return tty

    def generate_networks(self) -> IntermediateNetworks:
        """Generates value for networks parameter."""
        networks = self._config_model.required_networks
        self._logging_client.log_networks(networks)
        return networks

    def generate_healthcheck(self) -> Optional[IntermediateHealthcheck]:
        """Check to see if smoothie service has established connection to the emulator proxy."""
        return None

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        return None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        return self._monorepo_source.generate_emulator_mount_strings()

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = None
        self._logging_client.log_ports(ports)
        return ports

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        robot = self._ot2
        env_vars: IntermediateEnvironmentVariables = get_robot_pipettes(
            robot.hardware, robot.left_pipette, robot.right_pipette
        ).get_ot2_pipette_env_var(self.SMOOTHIE_DEFAULT_PORT)

        assert isinstance(self._config_model.robot, OT2InputModel)
        if self._config_model.robot.smoothie_env_vars is not None:
            env_vars.update(self._config_model.robot.smoothie_env_vars)

        self._logging_client.log_env_vars(env_vars)
        return env_vars
