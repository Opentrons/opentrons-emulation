from dataclasses import dataclass
from typing import Optional, TypeVar, Type

from tests.e2e.fixtures.e2e_system import E2EHostSystem
from tests.e2e.fixtures.expected_bind_mounts import ExpectedBindMounts
from tests.e2e.fixtures.module_containers import ModuleContainers

from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.consts import (

    ENTRYPOINT_MOUNT,
    MONOREPO_WHEELS,
    OT3FirmwareBuilderNamedVolumesMap,
    OT3FirmwareEmulatorNamedVolumesMap,
    STATE_MANAGER_VENV_VOLUME, OT3FirmwareExpectedBinaryNames,
)
from tests.e2e.utilities.helper_functions import (
    confirm_mount_exists,
    confirm_named_volume_exists, exec_in_container,
)

from abc import ABC, abstractmethod

from tests.e2e.utilities.system_test_definition import SystemTestDefinition

TResults = TypeVar("TResults", bound="Results")

@dataclass
class ResultsABC(ABC):

    @classmethod
    @abstractmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        ...

    @classmethod
    @abstractmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        ...


@dataclass
class OT3EmulatorContainers(ResultsABC):
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
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return (
            OT3EmulatorContainers(
                state_manager_exists=True,
                head_exists=True,
                gantry_x_exists=True,
                gantry_y_exists=True,
                gripper_exists=True,
                pipettes_exists=True,
                bootloader_exists=True,
                robot_server_exists=True,
                emulator_proxy_exists=True,
                can_server_exists=True,
            )
            if system_test_def.ot3_firmware_builder_created
            else OT3EmulatorContainers(
                state_manager_exists=False,
                head_exists=False,
                gantry_x_exists=False,
                gantry_y_exists=False,
                gripper_exists=False,
                pipettes_exists=False,
                bootloader_exists=False,
                robot_server_exists=False,
                emulator_proxy_exists=False,
                can_server_exists=False,
            )
        )
    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            state_manager_exists=system_under_test.ot3_containers.state_manager is not None,
            head_exists=system_under_test.ot3_containers.head is not None,
            gantry_x_exists=system_under_test.ot3_containers.gantry_x is not None,
            gantry_y_exists=system_under_test.ot3_containers.gantry_y is not None,
            gripper_exists=system_under_test.ot3_containers.gripper is not None,
            pipettes_exists=system_under_test.ot3_containers.pipettes is not None,
            bootloader_exists=system_under_test.ot3_containers.bootloader is not None,
            robot_server_exists=system_under_test.ot3_containers.robot_server is not None,
            emulator_proxy_exists=system_under_test.ot3_containers.emulator_proxy is not None,
            can_server_exists=system_under_test.ot3_containers.can_server is not None,
        )

@dataclass
class OT3EmulatorNamedVolumes(ResultsABC):

    head_volume_exists: bool
    gantry_x_volume_exists: bool
    gantry_y_volume_exists: bool
    gripper_volume_exists: bool
    pipettes_volume_exists: bool
    bootloader_volume_exists: bool

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            head_volume_exists=True,
            gantry_x_volume_exists=True,
            gantry_y_volume_exists=True,
            gripper_volume_exists=True,
            pipettes_volume_exists=True,
            bootloader_volume_exists=True
        )

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            head_volume_exists=confirm_named_volume_exists(
                system_under_test.ot3_containers.head,
                OT3FirmwareEmulatorNamedVolumesMap.HEAD
            ),
            gantry_x_volume_exists=confirm_named_volume_exists(
                system_under_test.ot3_containers.gantry_x,
                OT3FirmwareEmulatorNamedVolumesMap.GANTRY_X
            ),
            gantry_y_volume_exists=confirm_named_volume_exists(
                system_under_test.ot3_containers.gantry_y,
                OT3FirmwareEmulatorNamedVolumesMap.GANTRY_Y
            ),
            gripper_volume_exists=confirm_named_volume_exists(
                system_under_test.ot3_containers.gripper,
                OT3FirmwareEmulatorNamedVolumesMap.GRIPPER
            ),
            pipettes_volume_exists=confirm_named_volume_exists(
                system_under_test.ot3_containers.pipettes,
                OT3FirmwareEmulatorNamedVolumesMap.PIPETTES
            ),
            bootloader_volume_exists=confirm_named_volume_exists(
                system_under_test.ot3_containers.bootloader,
                OT3FirmwareEmulatorNamedVolumesMap.BOOTLOADER
            )
        )


@dataclass
class OT3StateManagerNamedVolumes(ResultsABC):

    state_manager_monorepo_exists: bool
    state_manager_virtual_env_exists: bool

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
           state_manager_monorepo_exists=confirm_named_volume_exists(
               container=system_under_test.ot3_containers.state_manager,
               expected_vol=MONOREPO_WHEELS
           ),
            state_manager_virtual_env_exists=confirm_named_volume_exists(
                container=system_under_test.ot3_containers.state_manager,
                expected_vol=STATE_MANAGER_VENV_VOLUME
            )
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            state_manager_monorepo_exists=True,
            state_manager_virtual_env_exists=True
        )


@dataclass
class OT3EmulatorMounts(ResultsABC):
    head_has_entrypoint_script: bool
    gantry_x_has_entrypoint_script: bool
    gantry_y_has_entrypoint_script: bool
    gripper_has_entrypoint_script: bool
    pipettes_has_entrypoint_script: bool
    bootloader_has_entrypoint_script: bool

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            head_has_entrypoint_script=confirm_mount_exists(system_under_test.ot3_containers.head, ENTRYPOINT_MOUNT),
            gantry_x_has_entrypoint_script=confirm_mount_exists(system_under_test.ot3_containers.gantry_x, ENTRYPOINT_MOUNT),
            gantry_y_has_entrypoint_script=confirm_mount_exists(system_under_test.ot3_containers.gantry_y, ENTRYPOINT_MOUNT),
            gripper_has_entrypoint_script=confirm_mount_exists(system_under_test.ot3_containers.gripper, ENTRYPOINT_MOUNT),
            pipettes_has_entrypoint_script=confirm_mount_exists(system_under_test.ot3_containers.pipettes, ENTRYPOINT_MOUNT),
            bootloader_has_entrypoint_script=confirm_mount_exists(system_under_test.ot3_containers.bootloader, ENTRYPOINT_MOUNT),
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            head_has_entrypoint_script=True,
            gantry_x_has_entrypoint_script=True,
            gantry_y_has_entrypoint_script=True,
            gripper_has_entrypoint_script=True,
            pipettes_has_entrypoint_script=True,
            bootloader_has_entrypoint_script=True,
        )


@dataclass
class OT3FirmwareBuilderNamedVolumes(ResultsABC):

    head_volume_exists: bool
    gantry_x_volume_exists: bool
    gantry_y_volume_exists: bool
    gripper_volume_exists: bool
    pipettes_volume_exists: bool
    bootloader_volume_exists: bool

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            head_volume_exists=confirm_named_volume_exists(system_under_test.ot3_containers.firmware_builder, OT3FirmwareBuilderNamedVolumesMap.HEAD),
            gantry_x_volume_exists=confirm_named_volume_exists(system_under_test.ot3_containers.firmware_builder, OT3FirmwareBuilderNamedVolumesMap.GANTRY_X),
            gantry_y_volume_exists=confirm_named_volume_exists(system_under_test.ot3_containers.firmware_builder, OT3FirmwareBuilderNamedVolumesMap.GANTRY_Y),
            gripper_volume_exists=confirm_named_volume_exists(system_under_test.ot3_containers.firmware_builder, OT3FirmwareBuilderNamedVolumesMap.GRIPPER),
            pipettes_volume_exists=confirm_named_volume_exists(system_under_test.ot3_containers.firmware_builder, OT3FirmwareBuilderNamedVolumesMap.PIPETTES),
            bootloader_volume_exists=confirm_named_volume_exists(system_under_test.ot3_containers.firmware_builder, OT3FirmwareBuilderNamedVolumesMap.BOOTLOADER),
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            head_volume_exists=True,
            gantry_x_volume_exists=True,
            gantry_y_volume_exists=True,
            gripper_volume_exists=True,
            pipettes_volume_exists=True,
            bootloader_volume_exists=True,
        )


@dataclass
class OT3Binaries(ResultsABC):
    head_binary_name_is_correct: bool
    gantry_x_binary_name_is_correct: bool
    gantry_y_binary_name_is_correct: bool
    gripper_binary_name_is_correct: bool
    pipettes_binary_name_is_correct: bool
    bootloader_binary_name_is_correct: bool

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            head_binary_name_is_correct=True,
            gantry_x_binary_name_is_correct=True,
            gantry_y_binary_name_is_correct=True,
            gripper_binary_name_is_correct=True,
            pipettes_binary_name_is_correct=True,
            bootloader_binary_name_is_correct=True,
        )

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            head_binary_name_is_correct=exec_in_container(system_under_test.ot3_containers.head, "ls /executable") == OT3FirmwareExpectedBinaryNames.HEAD,
            gantry_x_binary_name_is_correct=exec_in_container(system_under_test.ot3_containers.gantry_x, "ls /executable") == OT3FirmwareExpectedBinaryNames.GANTRY_X,
            gantry_y_binary_name_is_correct=exec_in_container(system_under_test.ot3_containers.gantry_y, "ls /executable") == OT3FirmwareExpectedBinaryNames.GANTRY_Y,
            gripper_binary_name_is_correct=exec_in_container(system_under_test.ot3_containers.gripper, "ls /executable") == OT3FirmwareExpectedBinaryNames.GRIPPER,
            pipettes_binary_name_is_correct=exec_in_container(system_under_test.ot3_containers.pipettes, "ls /executable") == OT3FirmwareExpectedBinaryNames.PIPETTES,
            bootloader_binary_name_is_correct=exec_in_container(system_under_test.ot3_containers.bootloader, "ls /executable") == OT3FirmwareExpectedBinaryNames.BOOTLOADER,
        )

@dataclass
class ContainersWithMonorepoWheelVolume(ResultsABC):
    monorepo_builder_has_monorepo_wheel: bool
    emulator_proxy_has_monorepo_wheel: bool
    robot_server_has_monorepo_wheel: bool
    can_server_has_monorepo_wheel: bool
    state_manager_has_monorepo_wheel: bool

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            monorepo_builder_has_monorepo_wheel=True,
            emulator_proxy_has_monorepo_wheel=True,
            robot_server_has_monorepo_wheel=True,
            can_server_has_monorepo_wheel=True,
            state_manager_has_monorepo_wheel=True,
        )

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            monorepo_builder_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.monorepo_builder, MONOREPO_WHEELS),
            emulator_proxy_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.emulator_proxy, MONOREPO_WHEELS),
            robot_server_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.robot_server, MONOREPO_WHEELS),
            can_server_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.can_server, MONOREPO_WHEELS),
            state_manager_has_monorepo_wheel=confirm_named_volume_exists(system_under_test.ot3_containers.state_manager, MONOREPO_WHEELS),
        )


@dataclass
class BuilderContainers(ResultsABC):
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool
    monorepo_builder_created: bool

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            ot3_firmware_builder_created=system_under_test.ot3_containers.ot3_firmware_builder_created,
            opentrons_modules_builder_created=system_under_test.ot3_containers.opentrons_modules_builder_created,
            monorepo_builder_created=system_under_test.ot3_containers.monorepo_builder_created,
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            ot3_firmware_builder_created=system_test_def.ot3_firmware_builder_created,
            opentrons_modules_builder_created=system_test_def.opentrons_modules_builder_created,
            monorepo_builder_created=system_test_def.monorepo_builder_created
        )


@dataclass
class LocalMounts(ResultsABC):
    monorepo_mounted: bool
    ot3_firmware_mounted: bool
    opentrons_modules_mounted: bool

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            monorepo_mounted=system_under_test.ot3_containers.local_monorepo_mounted,
            ot3_firmware_mounted=system_under_test.ot3_containers.local_ot3_firmware_mounted,
            opentrons_modules_mounted=system_under_test.ot3_containers.local_opentrons_modules_mounted,
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            monorepo_mounted=system_test_def.local_monorepo_mounted,
            ot3_firmware_mounted=system_test_def.local_ot3_firmware_mounted,
            opentrons_modules_mounted=system_test_def.local_opentrons_modules_mounted
        )
@dataclass
class SystemBuildArgs(ResultsABC):
    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            monorepo_build_args=system_under_test.ot3_containers.monorepo_build_args,
            ot3_firmware_build_args=system_under_test.ot3_containers.ot3_firmware_build_args,
            opentrons_modules_build_args=system_under_test.ot3_containers.opentrons_modules_build_args
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            monorepo_build_args=system_test_def.monorepo_build_args,
            ot3_firmware_build_args=system_test_def.ot3_firmware_build_args,
            opentrons_modules_build_args=system_test_def.opentrons_modules_build_args,
        )

@dataclass
class OT3Results(ResultsABC):
    containers: OT3EmulatorContainers
    emulator_volumes: OT3EmulatorNamedVolumes
    state_manager_volumes: OT3StateManagerNamedVolumes
    emulator_mounts: OT3EmulatorMounts
    builder_named_volumes: OT3FirmwareBuilderNamedVolumes
    binaries: OT3Binaries

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            containers=OT3EmulatorContainers.get_actual_results(system_under_test),
            emulator_volumes=OT3EmulatorNamedVolumes.get_actual_results(system_under_test),
            state_manager_volumes=OT3StateManagerNamedVolumes.get_actual_results(system_under_test),
            emulator_mounts=OT3EmulatorMounts.get_actual_results(system_under_test),
            builder_named_volumes=OT3FirmwareBuilderNamedVolumes.get_actual_results(system_under_test),
            binaries=OT3Binaries.get_actual_results(system_under_test),
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            containers=OT3EmulatorContainers.get_expected_results(system_test_def),
            emulator_volumes=OT3EmulatorNamedVolumes.get_expected_results(system_test_def),
            state_manager_volumes=OT3StateManagerNamedVolumes.get_expected_results(system_test_def),
            emulator_mounts=OT3EmulatorMounts.get_expected_results(system_test_def),
            builder_named_volumes=OT3FirmwareBuilderNamedVolumes.get_expected_results(system_test_def),
            binaries=OT3Binaries.get_expected_results(system_test_def),
        )


@dataclass
class Result(ResultsABC):
    """Class containing all result values for e2e testing."""
    ot3_results: Optional[OT3Results]
    builder_containers: BuilderContainers
    local_mounts: LocalMounts
    system_build_args: SystemBuildArgs
    containers_with_monorepo_volumes: ContainersWithMonorepoWheelVolume

    @classmethod
    def get_actual_results(cls: Type[TResults], system_under_test: E2EHostSystem) -> TResults:
        return cls(
            ot3_results=OT3Results.get_actual_results(system_under_test),
            builder_containers=BuilderContainers.get_actual_results(system_under_test),
            local_mounts=LocalMounts.get_actual_results(system_under_test),
            system_build_args=SystemBuildArgs.get_actual_results(system_under_test),
            containers_with_monorepo_volumes=ContainersWithMonorepoWheelVolume.get_actual_results(system_under_test)
        )

    @classmethod
    def get_expected_results(cls: Type[TResults], system_test_def: SystemTestDefinition) -> TResults:
        return cls(
            ot3_results=(
                OT3Results.get_expected_results(system_test_def)
                if system_test_def.ot3_firmware_builder_created
                else None
            ),
            builder_containers=BuilderContainers.get_expected_results(system_test_def),
            local_mounts=LocalMounts.get_expected_results(system_test_def),
            system_build_args=SystemBuildArgs.get_expected_results(system_test_def),
            containers_with_monorepo_volumes=ContainersWithMonorepoWheelVolume.get_expected_results(system_test_def)
        )

class ResultBuilder:

    def __init__(self, ot3_system: E2EHostSystem, modules: ModuleContainers, local_mounts: ExpectedBindMounts) -> None:
        self._ot3_system =ot3_system
        self._modules =modules
        self._local_mounts =local_mounts
