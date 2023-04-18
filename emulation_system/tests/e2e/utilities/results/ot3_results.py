from dataclasses import dataclass
from typing import (
    List,
    Set,
    Type,
)

from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition
from tests.e2e.utilities.consts import (
    ENTRYPOINT_MOUNT,
    ExpectedMount,
    ExpectedNamedVolume,
    MONOREPO_WHEELS,
    OT3_FIRMWARE_NAMED_VOLUMES,
    STATE_MANAGER_VENV_VOLUME,
    OT3FirmwareEmulatorNamedVolumesMap,
    OT3FirmwareExpectedBinaryNames,
)
from tests.e2e.utilities.helper_functions import (
    confirm_mount_exists,
    confirm_named_volume_exists,
    exec_in_container,
    get_mounts,
    get_volumes,
)
from tests.e2e.utilities.results.results_abc import ResultsABC, TResults


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
    can_server_exists: bool

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
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
                can_server_exists=False,
            )
        )

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            state_manager_exists=system_under_test.ot3_containers.state_manager
            is not None,
            head_exists=system_under_test.ot3_containers.head is not None,
            gantry_x_exists=system_under_test.ot3_containers.gantry_x is not None,
            gantry_y_exists=system_under_test.ot3_containers.gantry_y is not None,
            gripper_exists=system_under_test.ot3_containers.gripper is not None,
            pipettes_exists=system_under_test.ot3_containers.pipettes is not None,
            bootloader_exists=system_under_test.ot3_containers.bootloader is not None,
            robot_server_exists=system_under_test.ot3_containers.robot_server
            is not None,
            can_server_exists=system_under_test.ot3_containers.can_server is not None,
        )


@dataclass
class OT3EmulatorNamedVolumes(ResultsABC):

    head_volumes: Set[ExpectedNamedVolume]
    gantry_x_volumes: Set[ExpectedNamedVolume]
    gantry_y_volumes: Set[ExpectedNamedVolume]
    gripper_volumes: Set[ExpectedNamedVolume]
    pipettes_volumes: Set[ExpectedNamedVolume]
    bootloader_volumes: Set[ExpectedNamedVolume]

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            head_volumes={OT3FirmwareEmulatorNamedVolumesMap.HEAD},
            gantry_x_volumes={OT3FirmwareEmulatorNamedVolumesMap.GANTRY_X},
            gantry_y_volumes={OT3FirmwareEmulatorNamedVolumesMap.GANTRY_Y},
            gripper_volumes={OT3FirmwareEmulatorNamedVolumesMap.GRIPPER},
            pipettes_volumes={OT3FirmwareEmulatorNamedVolumesMap.PIPETTES},
            bootloader_volumes={OT3FirmwareEmulatorNamedVolumesMap.BOOTLOADER},
        )

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            head_volumes=get_volumes(system_under_test.ot3_containers.head),
            gantry_x_volumes=get_volumes(system_under_test.ot3_containers.gantry_x),
            gantry_y_volumes=get_volumes(system_under_test.ot3_containers.gantry_y),
            gripper_volumes=get_volumes(system_under_test.ot3_containers.gripper),
            pipettes_volumes=get_volumes(system_under_test.ot3_containers.pipettes),
            bootloader_volumes=get_volumes(system_under_test.ot3_containers.bootloader),
        )


@dataclass
class OT3StateManagerNamedVolumes(ResultsABC):

    volumes: Set[ExpectedNamedVolume]

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            volumes=get_volumes(system_under_test.ot3_containers.state_manager)
        )

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            volumes={MONOREPO_WHEELS, STATE_MANAGER_VENV_VOLUME}
        )


@dataclass
class OT3EmulatorMounts(ResultsABC):
    head_mounts: Set[ExpectedMount]
    gantry_x_mounts: Set[ExpectedMount]
    gantry_y_mounts: Set[ExpectedMount]
    gripper_mounts: Set[ExpectedMount]
    pipettes_mounts: Set[ExpectedMount]
    bootloader_mounts: Set[ExpectedMount]

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            head_mounts=get_mounts(system_under_test.ot3_containers.head),
            gantry_x_mounts=get_mounts(system_under_test.ot3_containers.gantry_x),
            gantry_y_mounts=get_mounts(system_under_test.ot3_containers.gantry_y),
            gripper_mounts=get_mounts(system_under_test.ot3_containers.gripper),
            pipettes_mounts=get_mounts(system_under_test.ot3_containers.pipettes),
            bootloader_mounts=get_mounts(system_under_test.ot3_containers.bootloader),
        )

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            head_mounts={ENTRYPOINT_MOUNT},
            gantry_x_mounts={ENTRYPOINT_MOUNT},
            gantry_y_mounts={ENTRYPOINT_MOUNT},
            gripper_mounts={ENTRYPOINT_MOUNT},
            pipettes_mounts={ENTRYPOINT_MOUNT},
            bootloader_mounts={ENTRYPOINT_MOUNT},
        )


@dataclass
class OT3FirmwareBuilderNamedVolumes(ResultsABC):

    volumes: Set[ExpectedNamedVolume]

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(volumes=get_volumes(system_under_test.ot3_containers.firmware_builder))

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(volumes=OT3_FIRMWARE_NAMED_VOLUMES)


@dataclass
class OT3Binaries(ResultsABC):
    head_binary_name: str
    gantry_x_binary_name: str
    gantry_y_binary_name: str
    gripper_binary_name: str
    pipettes_binary_name: str
    bootloader_binary_name: str

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            head_binary_name=OT3FirmwareExpectedBinaryNames.HEAD,
            gantry_x_binary_name=OT3FirmwareExpectedBinaryNames.GANTRY_X,
            gantry_y_binary_name=OT3FirmwareExpectedBinaryNames.GANTRY_Y,
            gripper_binary_name=OT3FirmwareExpectedBinaryNames.GRIPPER,
            pipettes_binary_name=OT3FirmwareExpectedBinaryNames.PIPETTES,
            bootloader_binary_name=OT3FirmwareExpectedBinaryNames.BOOTLOADER,
        )

    @classmethod
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            head_binary_name=exec_in_container(system_under_test.ot3_containers.head, "ls /executable"),
            gantry_x_binary_name=exec_in_container(system_under_test.ot3_containers.gantry_x, "ls /executable"),
            gantry_y_binary_name=exec_in_container(system_under_test.ot3_containers.gantry_y, "ls /executable"),
            gripper_binary_name=exec_in_container(system_under_test.ot3_containers.gripper, "ls /executable"),
            pipettes_binary_name=exec_in_container(system_under_test.ot3_containers.pipettes, "ls /executable"),
            bootloader_binary_name=exec_in_container(system_under_test.ot3_containers.bootloader, "ls /executable"),
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
    def get_actual_results(
        cls: Type[TResults], system_under_test: E2EHostSystem
    ) -> TResults:
        return cls(
            containers=OT3EmulatorContainers.get_actual_results(system_under_test),
            emulator_volumes=OT3EmulatorNamedVolumes.get_actual_results(
                system_under_test
            ),
            state_manager_volumes=OT3StateManagerNamedVolumes.get_actual_results(
                system_under_test
            ),
            emulator_mounts=OT3EmulatorMounts.get_actual_results(system_under_test),
            builder_named_volumes=OT3FirmwareBuilderNamedVolumes.get_actual_results(
                system_under_test
            ),
            binaries=OT3Binaries.get_actual_results(system_under_test),
        )

    @classmethod
    def get_expected_results(
        cls: Type[TResults], system_test_def: SystemTestDefinition
    ) -> TResults:
        return cls(
            containers=OT3EmulatorContainers.get_expected_results(system_test_def),
            emulator_volumes=OT3EmulatorNamedVolumes.get_expected_results(
                system_test_def
            ),
            state_manager_volumes=OT3StateManagerNamedVolumes.get_expected_results(
                system_test_def
            ),
            emulator_mounts=OT3EmulatorMounts.get_expected_results(system_test_def),
            builder_named_volumes=OT3FirmwareBuilderNamedVolumes.get_expected_results(
                system_test_def
            ),
            binaries=OT3Binaries.get_expected_results(system_test_def),
        )
