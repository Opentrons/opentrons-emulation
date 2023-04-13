from dataclasses import dataclass, fields
from typing import Optional

from tests.e2e.fixtures.ot3_containers import OT3SystemUnderTest
from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.consts import (
    CommonNamedVolumes,
    ENTRYPOINT_MOUNT,
    ExpectedNamedVolume,
    ExpectedMount,
    OT3FirmwareEmulatorNamedVolumesMap,
    STATE_MANAGER_VENV_VOLUME,
)
from tests.e2e.utilities.helper_functions import (
    confirm_mount_exists,
    confirm_named_volume_exists,
)


@dataclass
class OT3EmulatorContainers:
    state_manager_exists: bool
    head_exists: bool
    gantry_x_exists: bool
    gantry_y_exists: bool
    gripper_exists: bool
    pipettes_exists: bool
    bootloader_exists: bool
    robot_server_exists: bool
    emulator_proxy_exists: bool
    can_server_exists: bool

    @classmethod
    def init_all_exists(cls) -> "OT3EmulatorContainers":
        return cls(**{field.name: True for field in fields(cls)})

    @classmethod
    def init_all_not_exists(cls) -> "OT3EmulatorContainers":
        return cls(**{field.name: False for field in fields(cls)})

    @classmethod
    def from_system_under_test(
        cls, system_under_test: OT3SystemUnderTest
    ) -> "OT3EmulatorContainers":
        return cls(
        state_manager_exists=system_under_test.state_manager is not None,
        head_exists=system_under_test.head is not None,
        gantry_x_exists=system_under_test.gantry_x is not None,
        gantry_y_exists=system_under_test.gantry_y is not None,
        gripper_exists=system_under_test.gripper is not None,
        pipettes_exists=system_under_test.pipettes is not None,
        bootloader_exists=system_under_test.bootloader is not None,
        robot_server_exists=system_under_test.robot_server is not None,
        emulator_proxy_exists=system_under_test.emulator_proxy is not None,
        can_server_exists=system_under_test.can_server is not None,
        )




@dataclass
class OT3Binaries:
    head_binary_name: str
    gantry_x_binary_name: str
    gantry_y_binary_name: str
    gripper_binary_name: str
    pipettes_binary_name: str
    bootloader_binary_name: str

@dataclass
class OT3Mounts:
    gripper_entrypoint_mount: ExpectedMount
    gantry_x_entrypoint_mount: ExpectedMount
    gantry_y_entrypoint_mount: ExpectedMount
    head_entrypoint_mount: ExpectedMount
    pipettes_entrypoint_mount: ExpectedMount
    bootloader_entrypoint_mount: ExpectedMount
    robot_server_entrypoint_mount: ExpectedMount
    can_server_entrypoint_mount: ExpectedMount
    emulator_proxy_entrypoint_mount: ExpectedMount


@dataclass
class OT3EmulatorNamedVolumes:

    head_volume_exists: bool
    gantry_x_volume_exists: bool
    gantry_y_volume_exists: bool
    gripper_volume_exists: bool
    pipettes_volume_exists: bool
    bootloader_volume_exists: bool

    @classmethod
    def from_system_under_test(
        cls, system_under_test: OT3SystemUnderTest
    ) -> "OT3EmulatorNamedVolumes":
        return cls(
            head_volume_exists=confirm_named_volume_exists(
                system_under_test.head,
                OT3FirmwareEmulatorNamedVolumesMap.HEAD
            ),
            gantry_x_volume_exists=confirm_named_volume_exists(
                system_under_test.gantry_x,
                OT3FirmwareEmulatorNamedVolumesMap.GANTRY_X
            ),
            gantry_y_volume_exists=confirm_named_volume_exists(
                system_under_test.gantry_y,
                OT3FirmwareEmulatorNamedVolumesMap.GANTRY_Y
            ),
            gripper_volume_exists=confirm_named_volume_exists(
                system_under_test.gripper,
                OT3FirmwareEmulatorNamedVolumesMap.GRIPPER
            ),
            pipettes_volume_exists=confirm_named_volume_exists(
                system_under_test.pipettes,
                OT3FirmwareEmulatorNamedVolumesMap.PIPETTES
            ),
            bootloader_volume_exists=confirm_named_volume_exists(
                system_under_test.bootloader,
                OT3FirmwareEmulatorNamedVolumesMap.BOOTLOADER
            )
        )


@dataclass
class OT3StateManagerNamedVolumes:

    state_manager_monorepo_exists: bool
    state_manager_virtual_env_exists: bool

    @classmethod
    def from_system_under_test(
        cls, system_under_test: OT3SystemUnderTest
    ) -> "OT3StateManagerNamedVolumes":
        return cls(
           state_manager_monorepo_exists=confirm_named_volume_exists(
               container=system_under_test.state_manager,
               expected_vol=CommonNamedVolumes.MONOREPO_WHEELS
           ),
            state_manager_virtual_env_exists=confirm_named_volume_exists(
                container=system_under_test.state_manager,
                expected_vol=STATE_MANAGER_VENV_VOLUME
            )
        )


@dataclass
class OT3EmulatorMounts:
    head_has_entrypoint_script: bool
    gantry_x_has_entrypoint_script: bool
    gantry_y_has_entrypoint_script: bool
    gripper_has_entrypoint_script: bool
    pipettes_has_entrypoint_script: bool
    bootloader_has_entrypoint_script: bool

    @classmethod
    def from_system_under_test(cls, system_under_test: OT3SystemUnderTest):
        return cls(
            head_has_entrypoint_script=confirm_mount_exists(system_under_test.head, ENTRYPOINT_MOUNT),
            gantry_x_has_entrypoint_script=confirm_mount_exists(system_under_test.gantry_x, ENTRYPOINT_MOUNT),
            gantry_y_has_entrypoint_script=confirm_mount_exists(system_under_test.gantry_y, ENTRYPOINT_MOUNT),
            gripper_has_entrypoint_script=confirm_mount_exists(system_under_test.gripper, ENTRYPOINT_MOUNT),
            pipettes_has_entrypoint_script=confirm_mount_exists(system_under_test.pipettes, ENTRYPOINT_MOUNT),
            bootloader_has_entrypoint_script=confirm_mount_exists(system_under_test.bootloader, ENTRYPOINT_MOUNT),
        )


@dataclass
class OT3FirmwareBuilderNamedVolumes:

    ot3_firmware_builder_head: ExpectedNamedVolume
    ot3_firmware_builder_gantry_x: ExpectedNamedVolume
    ot3_firmware_builder_gantry_y: ExpectedNamedVolume
    ot3_firmware_builder_gripper: ExpectedNamedVolume
    ot3_firmware_builder_pipettes: ExpectedNamedVolume
    ot3_firmware_builder_bootloader: ExpectedNamedVolume

@dataclass
class OT3ContainersWithMonorepoWheelVolume:
    monorepo_builder: ExpectedNamedVolume
    emulator_proxy: ExpectedNamedVolume
    robot_server: ExpectedNamedVolume
    can_server: ExpectedNamedVolume
    state_manager: ExpectedNamedVolume




@dataclass
class BuilderContainers:
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool
    monorepo_builder_created: bool

    @classmethod
    def from_system_under_test(
        cls, system_under_test: OT3SystemUnderTest
    ) -> "BuilderContainers":
        return cls(
            ot3_firmware_builder_created=system_under_test.ot3_firmware_builder_created,
            opentrons_modules_builder_created=system_under_test.opentrons_modules_builder_created,
            monorepo_builder_created=system_under_test.monorepo_builder_created,
        )

@dataclass
class LocalMounts:
    monorepo_mounted: bool
    ot3_firmware_mounted: bool
    opentrons_modules_mounted: bool

    @classmethod
    def from_system_under_test(
        cls,
        system_under_test: OT3SystemUnderTest
    ) -> "LocalMounts":
        return cls(
            monorepo_mounted=system_under_test.local_monorepo_mounted,
            ot3_firmware_mounted=system_under_test.local_ot3_firmware_mounted,
            opentrons_modules_mounted=system_under_test.local_opentrons_modules_mounted,
        )

@dataclass
class SystemBuildArgs:
    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations

    @classmethod
    def from_system_under_test(
        cls,
        system_under_test: OT3SystemUnderTest
    ) -> "SystemBuildArgs":
        return cls(
            monorepo_build_args=system_under_test.monorepo_build_args,
            ot3_firmware_build_args=system_under_test.ot3_firmware_build_args,
            opentrons_modules_build_args=system_under_test.opentrons_modules_build_args
        )

@dataclass
class OT3Results:
    containers: OT3EmulatorContainers
    emulator_volumes: OT3EmulatorNamedVolumes
    state_manager_volumes: OT3StateManagerNamedVolumes
    emulator_mounts: OT3EmulatorMounts
    # binaries: OT3Binaries
    # containers_with_monorepo_volumes: OT3ContainersWithMonorepoWheelVolume


@dataclass
class Result:
    """Class containing all result values for e2e testing."""
    ot3_results: Optional[OT3Results]
    builder_containers: BuilderContainers
    local_mounts: LocalMounts
    system_build_args: SystemBuildArgs
