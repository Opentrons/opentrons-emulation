"""Results classes extending ResultsABC, representing expected and actual of OT-3 Containers."""

from dataclasses import dataclass
from typing import Set, Type

from docker.models.containers import Container  # type: ignore[import]

from tests.e2e.consts import (
    ENTRYPOINT_MOUNT,
    MONOREPO_WHEEL_VOLUME,
    OT3_FIRMWARE_BUILDER_NAMED_VOLUMES,
    STATE_MANAGER_VENV_VOLUME,
    STATE_MANAGER_WHEEL_VOLUME,
    BindMountInfo,
    NamedVolumeInfo,
    OT3FirmwareEmulatorNamedVolumesMap,
    OT3FirmwareExpectedBinaryNames,
)
from tests.e2e.docker_interface.e2e_system import E2EHostSystem
from tests.e2e.helper_functions import exec_in_container, get_mounts, get_volumes
from tests.e2e.results.results_abc import ResultABC
from tests.e2e.test_definition.system_test_definition import SystemTestDefinition


@dataclass
class OT3EmulatorContainers(ResultABC):
    """Validate existence of all OT-3 containers."""

    state_manager_exists: bool
    head_exists: bool
    gantry_x_exists: bool
    gantry_y_exists: bool
    gripper_exists: bool
    left_pipette_exists: bool
    right_pipette_exists: bool
    bootloader_exists: bool
    can_server_exists: bool

    @classmethod
    def get_expected_results(
        cls: Type["OT3EmulatorContainers"], system_test_def: SystemTestDefinition
    ) -> "OT3EmulatorContainers":
        """If ot3-firmware-builder created everything is expected to exist.

        Otherwise, nothing exists.
        """
        return (
            cls(
                state_manager_exists=True,
                head_exists=True,
                gantry_x_exists=True,
                gantry_y_exists=True,
                gripper_exists=True,
                left_pipette_exists=True,
                right_pipette_exists=True,
                bootloader_exists=True,
                can_server_exists=True,
            )
            if system_test_def.ot3_firmware_builder_created
            else cls(
                state_manager_exists=False,
                head_exists=False,
                gantry_x_exists=False,
                gantry_y_exists=False,
                gripper_exists=False,
                left_pipette_exists=False,
                right_pipette_exists=False,
                bootloader_exists=False,
                can_server_exists=False,
            )
        )

    @classmethod
    def get_actual_results(
        cls: Type["OT3EmulatorContainers"], system_under_test: E2EHostSystem
    ) -> "OT3EmulatorContainers":
        """Validate all containers in system under test exist."""
        return cls(
            state_manager_exists=system_under_test.ot3_containers.state_manager
            is not None,
            head_exists=system_under_test.ot3_containers.head is not None,
            gantry_x_exists=system_under_test.ot3_containers.gantry_x is not None,
            gantry_y_exists=system_under_test.ot3_containers.gantry_y is not None,
            gripper_exists=system_under_test.ot3_containers.gripper is not None,
            left_pipette_exists=system_under_test.ot3_containers.left_pipette
            is not None,
            right_pipette_exists=system_under_test.ot3_containers.right_pipette
            is not None,
            bootloader_exists=system_under_test.ot3_containers.bootloader is not None,
            can_server_exists=system_under_test.ot3_containers.can_server is not None,
        )


@dataclass
class OT3EmulatorNamedVolumes(ResultABC):
    """Validate that all expected named volumes exist for each container."""

    head_volumes: Set[NamedVolumeInfo]
    gantry_x_volumes: Set[NamedVolumeInfo]
    gantry_y_volumes: Set[NamedVolumeInfo]
    gripper_volumes: Set[NamedVolumeInfo]
    left_pipette_volumes: Set[NamedVolumeInfo]
    right_pipette_volumes: Set[NamedVolumeInfo]
    bootloader_volumes: Set[NamedVolumeInfo]

    @classmethod
    def get_expected_results(
        cls: Type["OT3EmulatorNamedVolumes"], system_test_def: SystemTestDefinition
    ) -> "OT3EmulatorNamedVolumes":
        """Validate each emulator has their binary volume mounted."""
        return cls(
            head_volumes={OT3FirmwareEmulatorNamedVolumesMap.HEAD},
            gantry_x_volumes={OT3FirmwareEmulatorNamedVolumesMap.GANTRY_X},
            gantry_y_volumes={OT3FirmwareEmulatorNamedVolumesMap.GANTRY_Y},
            gripper_volumes=OT3FirmwareEmulatorNamedVolumesMap.GRIPPER,
            left_pipette_volumes=OT3FirmwareEmulatorNamedVolumesMap.LEFT_PIPETTE,
            right_pipette_volumes=OT3FirmwareEmulatorNamedVolumesMap.RIGHT_PIPETTE,
            bootloader_volumes={OT3FirmwareEmulatorNamedVolumesMap.BOOTLOADER},
        )

    @classmethod
    def get_actual_results(
        cls: Type["OT3EmulatorNamedVolumes"], system_under_test: E2EHostSystem
    ) -> "OT3EmulatorNamedVolumes":
        """Get all volumes for each container."""
        return cls(
            head_volumes=get_volumes(system_under_test.ot3_containers.head),
            gantry_x_volumes=get_volumes(system_under_test.ot3_containers.gantry_x),
            gantry_y_volumes=get_volumes(system_under_test.ot3_containers.gantry_y),
            gripper_volumes=get_volumes(system_under_test.ot3_containers.gripper),
            left_pipette_volumes=get_volumes(
                system_under_test.ot3_containers.left_pipette
            ),
            right_pipette_volumes=get_volumes(
                system_under_test.ot3_containers.right_pipette
            ),
            bootloader_volumes=get_volumes(system_under_test.ot3_containers.bootloader),
        )


@dataclass
class OT3StateManagerNamedVolumes(ResultABC):
    """Ensures that volumes on state manager are correct."""

    volumes: Set[NamedVolumeInfo]

    @classmethod
    def get_actual_results(
        cls: Type["OT3StateManagerNamedVolumes"], system_under_test: E2EHostSystem
    ) -> "OT3StateManagerNamedVolumes":
        """Load state manager volumes."""
        return cls(volumes=get_volumes(system_under_test.ot3_containers.state_manager))

    @classmethod
    def get_expected_results(
        cls: Type["OT3StateManagerNamedVolumes"], system_test_def: SystemTestDefinition
    ) -> "OT3StateManagerNamedVolumes":
        """Load expected state manager volumes."""
        return cls(
            volumes={
                MONOREPO_WHEEL_VOLUME,
                STATE_MANAGER_VENV_VOLUME,
                STATE_MANAGER_WHEEL_VOLUME,
            }
        )


@dataclass
class OT3EmulatorMounts(ResultABC):
    """Validates each emulator has entrypoint.sh bound to it."""

    head_mounts: Set[BindMountInfo]
    gantry_x_mounts: Set[BindMountInfo]
    gantry_y_mounts: Set[BindMountInfo]
    gripper_mounts: Set[BindMountInfo]
    left_pipette_mounts: Set[BindMountInfo]
    right_pipette_mounts: Set[BindMountInfo]
    bootloader_mounts: Set[BindMountInfo]

    @classmethod
    def get_actual_results(
        cls: Type["OT3EmulatorMounts"], system_under_test: E2EHostSystem
    ) -> "OT3EmulatorMounts":
        """Load mounts for each container."""
        return cls(
            head_mounts=get_mounts(system_under_test.ot3_containers.head),
            gantry_x_mounts=get_mounts(system_under_test.ot3_containers.gantry_x),
            gantry_y_mounts=get_mounts(system_under_test.ot3_containers.gantry_y),
            gripper_mounts=get_mounts(system_under_test.ot3_containers.gripper),
            left_pipette_mounts=get_mounts(
                system_under_test.ot3_containers.left_pipette
            ),
            right_pipette_mounts=get_mounts(
                system_under_test.ot3_containers.right_pipette
            ),
            bootloader_mounts=get_mounts(system_under_test.ot3_containers.bootloader),
        )

    @classmethod
    def get_expected_results(
        cls: Type["OT3EmulatorMounts"], system_test_def: SystemTestDefinition
    ) -> "OT3EmulatorMounts":
        """Create comparison sets, each containing entrypoint.sh."""
        return cls(
            head_mounts={ENTRYPOINT_MOUNT},
            gantry_x_mounts={ENTRYPOINT_MOUNT},
            gantry_y_mounts={ENTRYPOINT_MOUNT},
            gripper_mounts={ENTRYPOINT_MOUNT},
            left_pipette_mounts={ENTRYPOINT_MOUNT},
            right_pipette_mounts={ENTRYPOINT_MOUNT},
            bootloader_mounts={ENTRYPOINT_MOUNT},
        )


@dataclass
class OT3FirmwareBuilderNamedVolumes(ResultABC):
    """Validate that ot3-firmware-builder named volumes are correct."""

    volumes: Set[NamedVolumeInfo]

    @classmethod
    def get_actual_results(
        cls: Type["OT3FirmwareBuilderNamedVolumes"], system_under_test: E2EHostSystem
    ) -> "OT3FirmwareBuilderNamedVolumes":
        """Load ot3-firmware-builder named volumes."""
        return cls(
            volumes=get_volumes(system_under_test.ot3_containers.firmware_builder)
        )

    @classmethod
    def get_expected_results(
        cls: Type["OT3FirmwareBuilderNamedVolumes"],
        system_test_def: SystemTestDefinition,
    ) -> "OT3FirmwareBuilderNamedVolumes":
        """Generate set of expected volumes for ot3-firmware-builder.

        Expected to contain the following:
        All executable volumes
        State Manager venv and wheel volumes
        build-host and stm32-tools cache overrides
        """
        return cls(volumes=OT3_FIRMWARE_BUILDER_NAMED_VOLUMES)


@dataclass
class OT3Binaries(ResultABC):
    """Validate each emulator's binary is named correctly."""

    head_binary_name: str
    gantry_x_binary_name: str
    gantry_y_binary_name: str
    gripper_binary_name: str
    left_pipette_binary_names: Set[str]
    right_pipette_binary_names: Set[str]
    bootloader_binary_name: str

    @classmethod
    def get_expected_results(
        cls: Type["OT3Binaries"], system_test_def: SystemTestDefinition
    ) -> "OT3Binaries":
        """Generate expected binary names."""
        return cls(
            head_binary_name=OT3FirmwareExpectedBinaryNames.HEAD,
            gantry_x_binary_name=OT3FirmwareExpectedBinaryNames.GANTRY_X,
            gantry_y_binary_name=OT3FirmwareExpectedBinaryNames.GANTRY_Y,
            gripper_binary_name=OT3FirmwareExpectedBinaryNames.GRIPPER,
            left_pipette_binary_names=OT3FirmwareExpectedBinaryNames.LEFT_PIPETTE,
            right_pipette_binary_names=OT3FirmwareExpectedBinaryNames.RIGHT_PIPETTE,
            bootloader_binary_name=OT3FirmwareExpectedBinaryNames.BOOTLOADER,
        )

    @classmethod
    def get_actual_results(
        cls: Type["OT3Binaries"], system_under_test: E2EHostSystem
    ) -> "OT3Binaries":
        """Load actual binary names."""
        return cls(
            head_binary_name=exec_in_container(
                system_under_test.ot3_containers.head, "ls /executable"
            ),
            gantry_x_binary_name=exec_in_container(
                system_under_test.ot3_containers.gantry_x, "ls /executable"
            ),
            gantry_y_binary_name=exec_in_container(
                system_under_test.ot3_containers.gantry_y, "ls /executable"
            ),
            gripper_binary_name=exec_in_container(
                system_under_test.ot3_containers.gripper, "ls /executable"
            ),
            left_pipette_binary_names=set(
                exec_in_container(
                    system_under_test.ot3_containers.left_pipette, "ls /executable"
                ).split("\n")
            ),
            right_pipette_binary_names=set(
                exec_in_container(
                    system_under_test.ot3_containers.right_pipette, "ls /executable"
                ).split("\n")
            ),
            bootloader_binary_name=exec_in_container(
                system_under_test.ot3_containers.bootloader, "ls /executable"
            ),
        )


@dataclass
class PipetteEeproms(ResultABC):
    """Validate that pipette eeproms are correct."""

    left_pipette_eeprom_file_has_content: bool
    right_pipette_eeprom_file_has_content: bool

    @staticmethod
    def _file_has_content(container: Container) -> bool:
        return int(exec_in_container(container, "stat -c %s /eeprom/eeprom.bin")) > 0

    @classmethod
    def get_expected_results(
        cls: Type["PipetteEeproms"], system_test_def: SystemTestDefinition
    ) -> "PipetteEeproms":
        """Generate expected pipette eeproms."""
        return cls(
            left_pipette_eeprom_file_has_content=system_test_def.left_pipette_expected,
            right_pipette_eeprom_file_has_content=system_test_def.right_pipette_expected,
        )

    @classmethod
    def get_actual_results(
        cls: Type["PipetteEeproms"], system_under_test: E2EHostSystem
    ) -> "PipetteEeproms":
        """Load actual pipette eeproms."""
        return cls(
            left_pipette_eeprom_file_has_content=cls._file_has_content(
                system_under_test.ot3_containers.left_pipette
            ),
            right_pipette_eeprom_file_has_content=cls._file_has_content(
                system_under_test.ot3_containers.right_pipette
            ),
        )


@dataclass
class OT3Result(ResultABC):
    """Collect all ot3 result classes into a single dataclass."""

    containers: OT3EmulatorContainers
    emulator_volumes: OT3EmulatorNamedVolumes
    state_manager_volumes: OT3StateManagerNamedVolumes
    emulator_mounts: OT3EmulatorMounts
    builder_named_volumes: OT3FirmwareBuilderNamedVolumes
    binaries: OT3Binaries
    pipette_eeproms: PipetteEeproms

    @classmethod
    def get_actual_results(
        cls: Type["OT3Result"], system_under_test: E2EHostSystem
    ) -> "OT3Result":
        """Get ot3_result actual resutls."""
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
            pipette_eeproms=PipetteEeproms.get_actual_results(system_under_test),
        )

    @classmethod
    def get_expected_results(
        cls: Type["OT3Result"], system_test_def: SystemTestDefinition
    ) -> "OT3Result":
        """Get OT3Result expected results."""
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
            pipette_eeproms=PipetteEeproms.get_expected_results(system_test_def),
        )
