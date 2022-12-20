"""Module containing ConcreteSmoothieServiceBuilder."""
import json
from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.images import SmoothieImage
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.consts import MONOREPO_NAMED_VOLUME_STRING

from ...input.hardware_models import OT2InputModel
from ...logging import SmoothieLoggingClient
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteSmoothieServiceBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building a Smoothie Service."""

    SMOOTHIE_NAME = "smoothie"
    SMOOTHIE_DEFAULT_PORT = 11000

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a ConcreteSmoothieServiceBuilder object."""
        super().__init__(config_model, global_settings, dev)
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
        image_name = SmoothieImage().image_name
        # self._logging_client.log_image_name(image_name, source_type, "source-type")
        return image_name

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
        return [self.ENTRYPOINT_MOUNT_STRING, MONOREPO_NAMED_VOLUME_STRING]

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        command = None
        self._logging_client.log_command(command)
        return command

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        ports = None
        self._logging_client.log_ports(ports)
        return ports

    def generate_depends_on(self) -> Optional[IntermediateDependsOn]:
        """Generates value for depends_on parameter."""
        depends_on = None
        self._logging_client.log_depends_on(depends_on)
        return depends_on

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        inner_env_vars = self._ot2.hardware_specific_attributes.dict()
        inner_env_vars["port"] = self.SMOOTHIE_DEFAULT_PORT
        env_vars: IntermediateEnvironmentVariables = {
            "OT_EMULATOR_smoothie": json.dumps(inner_env_vars)
        }

        assert isinstance(self._config_model.robot, OT2InputModel)
        if self._config_model.robot.smoothie_env_vars is not None:
            print(self._config_model.robot.smoothie_env_vars)
            # env_vars.update()

        self._logging_client.log_env_vars(env_vars)
        return env_vars
