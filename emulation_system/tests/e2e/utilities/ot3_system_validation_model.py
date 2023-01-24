import os
from dataclasses import dataclass

from e2e.utilities.build_arg_configurations import BuildArgConfigurations
from e2e.utilities.helper_functions import (
    mount_exists,
    named_volume_exists,
)
from e2e.utilities.ot3_system import OT3System
from emulation_system.consts import DOCKERFILE_DIR_LOCATION


@dataclass
class OT3SystemValidationModel:
    monorepo_builder_created: bool
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool

    local_monorepo_mounted: bool
    local_ot3_firmware_mounted: bool
    local_opentrons_modules_mounted: bool

    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations

    def _confirm_created_builders(self, ot3_system: OT3System) -> None:
        assert ot3_system.monorepo_builder_created == self.monorepo_builder_created
        assert (
                ot3_system.ot3_firmware_builder_created == self.ot3_firmware_builder_created
        )
        assert (
                ot3_system.opentrons_modules_builder_created
                == self.opentrons_modules_builder_created
        )

    def _confirm_local_mounts(self, ot3_system: OT3System) -> None:
        assert ot3_system.local_monorepo_mounted == self.local_monorepo_mounted
        assert ot3_system.local_ot3_firmware_mounted == self.local_ot3_firmware_mounted
        assert (
                ot3_system.local_opentrons_modules_mounted
                == self.local_opentrons_modules_mounted
        )

    def _confirm_build_args(self, ot3_system: OT3System) -> None:
        assert ot3_system.monorepo_build_args == self.monorepo_build_args
        assert ot3_system.ot3_firmware_build_args == self.ot3_firmware_build_args
        assert (
                ot3_system.opentrons_modules_build_args == self.opentrons_modules_build_args
        )

    def compare(self, ot3_system: OT3System) -> None:
        self._confirm_created_builders(ot3_system)
        self._confirm_local_mounts(ot3_system)
        self._confirm_build_args(ot3_system)

        expected_containers_w_entrypoint_script = [
            ot3_system.gantry_x,
            ot3_system.gantry_y,
            ot3_system.head,
            ot3_system.gripper,
            ot3_system.pipettes,
            ot3_system.bootloader,
            ot3_system.state_manager,
            ot3_system.robot_server,
            ot3_system.can_server,
            ot3_system.emulator_proxy,
        ]
        for container in expected_containers_w_entrypoint_script:
            assert mount_exists(
                container,
                os.path.join(DOCKERFILE_DIR_LOCATION, "entrypoint.sh"),
                "/entrypoint.sh",
            )

        if self.monorepo_builder_created:
            expected_containers_w_monorepo_wheel_volume = [
                ot3_system.monorepo_builder,
                ot3_system.emulator_proxy,
                ot3_system.robot_server,
                ot3_system.state_manager,
                ot3_system.can_server,
            ]
            for container in expected_containers_w_monorepo_wheel_volume:
                assert named_volume_exists(container, "monorepo-wheels", "/dist")
