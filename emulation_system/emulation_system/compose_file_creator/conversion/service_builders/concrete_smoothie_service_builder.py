"""Module containing ConcreteSmoothieServiceBuilder."""
import json
from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.images import SmoothieImages
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateDependsOn,
    IntermediateEnvironmentVariables,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.compose_file_creator.utilities.shared_functions import (
    add_opentrons_named_volumes,
    get_build_args,
    get_entrypoint_mount_string,
)

from ...logging import SmoothieLoggingClient
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteSmoothieServiceBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building a Smoothie Service."""

    SMOOTHIE_NAME = "smoothie"

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a ConcreteSmoothieServiceBuilder object."""
        super().__init__(config_model, global_settings)
        self._dev = dev
        self._ot2 = self.get_ot2(config_model)
        self._logging_client = SmoothieLoggingClient(self._dev)
        self._image = self._generate_image()

    def _generate_image(self) -> str:
        """Inner method for generating image.

        Using an inner method and setting the value to self._image so when other
        methods need to access the image, this function is not called again.
        This prevents, primarily, logging happening twice, but also the increased
        overhead of calculating the same thing twice.
        """
        smoothie_images = SmoothieImages()
        source_type = self._ot2.source_type
        image_name = (
            smoothie_images.local_firmware_image_name
            if source_type == SourceType.LOCAL
            else smoothie_images.remote_firmware_image_name
        )
        self._logging_client.log_image_name(image_name, source_type, "source-type")
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
        return f"{self._image}:latest"

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

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        repo = OpentronsRepository.OPENTRONS
        if self._ot2.source_type == SourceType.REMOTE:
            build_args = get_build_args(
                repo,
                self._ot2.source_location,
                self._global_settings.get_repo_commit(repo),
                self._global_settings.get_repo_head(repo),
            )

        else:
            build_args = None
        self._logging_client.log_build_args(build_args)
        return build_args

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        if self._ot2.source_type == SourceType.LOCAL:
            volumes = [get_entrypoint_mount_string()]
            volumes.extend(self._ot2.get_mount_strings())
            add_opentrons_named_volumes(volumes)
        else:
            volumes = None
        self._logging_client.log_volumes(volumes)
        return volumes

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
        inner_env_vars["port"] = 11000
        env_vars = {"OT_EMULATOR_smoothie": json.dumps(inner_env_vars)}
        self._logging_client.log_env_vars(env_vars)
        return env_vars
