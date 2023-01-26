"""Module containing ConcreteOT3ServiceBuilder class."""
from typing import Optional

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateCommand,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)

from ...images import OT3FirmwareBuilderImage
from ...utilities.shared_functions import get_build_args
from .abstract_service_builder import AbstractServiceBuilder


class ConcreteOT3FirmwareBuilderBuilder(AbstractServiceBuilder):
    """Concrete implementation of AbstractServiceBuilder for building ot3-firmware-builder Service."""

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        global_settings: OpentronsEmulationConfiguration,
        dev: bool,
    ) -> None:
        """Instantiates a ConcreteOT3ServiceBuilder object."""
        super().__init__(config_model, global_settings, dev)
        self._ot3 = self.get_ot3(self._config_model)

    @property
    def _image(self) -> str:
        return OT3FirmwareBuilderImage().image_name

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
            command="(cd /ot3-firmware) && (cd /opentrons)",
        )

    def generate_build_args(self) -> Optional[IntermediateBuildArgs]:
        """Generates value for build parameter."""
        build_args: IntermediateBuildArgs = {}
        if self._ot3_source.is_remote():
            ot3_firmware_build_args = get_build_args(
                self._ot3_source, self._global_settings
            )
            assert ot3_firmware_build_args is not None
            build_args.update(ot3_firmware_build_args)

        if self._monorepo_source.is_remote():
            monorepo_build_args = get_build_args(
                self._monorepo_source, self._global_settings
            )
            assert monorepo_build_args is not None
            build_args.update(monorepo_build_args)

        return build_args if len(build_args) > 0 else None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        volumes: IntermediateVolumes = [
            "state_manager_venv:/ot3-firmware/build-host/.venv",
        ]
        volumes.extend(self._ot3_source.generate_builder_mount_strings())

        return volumes

    def generate_command(self) -> Optional[IntermediateCommand]:
        """Generates value for command parameter."""
        return None

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        return None

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        return None
