"""Module containing OT3Services class."""
from typing import Optional

from emulation_system import SystemConfigurationModel
from emulation_system.compose_file_creator.pipette_utils import (
    get_robot_pipettes,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
    IntermediateEnvironmentVariables,
    IntermediateHealthcheck,
    IntermediateNetworks,
    IntermediatePorts,
    IntermediateVolumes,
)
from emulation_system.compose_file_creator.utilities.hardware_utils import is_ot3

from ...images import OT3FirmwareBuilderImage
from .abstract_service import AbstractService


class OT3FirmwareBuilderService(AbstractService):
    """Concrete implementation of AbstractService for building ot3-firmware-builder Service."""

    def __init__(
        self,
        config_model: SystemConfigurationModel,
        dev: bool,
    ) -> None:
        """Instantiates a OT3FirmwareBuilderService object."""
        super().__init__(config_model, dev)
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
        return self._config_model.required_networks

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
            ot3_firmware_build_args = self._ot3_source.generate_build_args()
            assert ot3_firmware_build_args is not None
            build_args.update(ot3_firmware_build_args)

        if self._monorepo_source.is_remote():
            monorepo_build_args = self._monorepo_source.generate_build_args()
            assert monorepo_build_args is not None
            build_args.update(monorepo_build_args)

        return build_args if len(build_args) > 0 else None

    def generate_volumes(self) -> Optional[IntermediateVolumes]:
        """Generates value for volumes parameter."""
        vols = self._ot3_source.generate_builder_mount_strings()
        if self._monorepo_source.is_local():
            vols.extend(self._monorepo_source.generate_source_code_bind_mounts())
        return vols

    def generate_ports(self) -> Optional[IntermediatePorts]:
        """Generates value for ports parameter."""
        return None

    def generate_env_vars(self) -> Optional[IntermediateEnvironmentVariables]:
        """Generates value for environment parameter."""
        robot = self._ot3
        env_vars: IntermediateEnvironmentVariables = {}
        pipettes = get_robot_pipettes(
            robot.hardware, robot.left_pipette, robot.right_pipette
        )

        if is_ot3(robot):
            env_vars = {
                "OPENTRONS_PROJECT": "ot3",
            }

        env_vars.update(pipettes.get_left_pipette_env_var())
        env_vars.update(pipettes.get_right_pipette_env_var())
        return env_vars
