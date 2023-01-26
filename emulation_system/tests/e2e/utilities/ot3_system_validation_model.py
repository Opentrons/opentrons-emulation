from dataclasses import dataclass

from e2e.utilities.consts import (
    CommonMounts,
    MonorepoBuilderNamedVolumes,
    OT3FirmwareBuilderNamedVolumes,
)

from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.helper_functions import mount_exists, named_volume_exists
from tests.e2e.utilities.ot3_system import OT3System


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

    @staticmethod
    def _confirm_ot3_emulator_named_volumes(ot3_system: OT3System) -> None:
        data = (
            (ot3_system.gantry_x, OT3FirmwareBuilderNamedVolumes.GANTRY_X),
            (ot3_system.gantry_y, OT3FirmwareBuilderNamedVolumes.GANTRY_Y),
            (ot3_system.head, OT3FirmwareBuilderNamedVolumes.HEAD),
            (ot3_system.gripper, OT3FirmwareBuilderNamedVolumes.GRIPPER),
            (ot3_system.pipettes, OT3FirmwareBuilderNamedVolumes.PIPETTES),
            (ot3_system.bootloader, OT3FirmwareBuilderNamedVolumes.BOOTLOADER),
        )
        for container, named_volume in data:
            assert named_volume_exists(container, named_volume)

    def compare(self, ot3_system: OT3System) -> None:
        self._confirm_created_builders(ot3_system)
        self._confirm_local_mounts(ot3_system)
        self._confirm_build_args(ot3_system)

        for container in ot3_system.containers_with_entrypoint_script:
            assert mount_exists(container, CommonMounts.ENTRYPOINT_MOUNT)

        if self.monorepo_builder_created:
            assert not mount_exists(
                ot3_system.monorepo_builder, CommonMounts.ENTRYPOINT_MOUNT
            )
            for container in ot3_system.containers_with_monorepo_wheel_volume:
                assert named_volume_exists(
                    container, MonorepoBuilderNamedVolumes.MONOREPO_WHEELS
                )

        if self.ot3_firmware_builder_created:
            assert not mount_exists(
                ot3_system.firmware_builder, CommonMounts.ENTRYPOINT_MOUNT
            )
            self._confirm_ot3_emulator_named_volumes(ot3_system)
