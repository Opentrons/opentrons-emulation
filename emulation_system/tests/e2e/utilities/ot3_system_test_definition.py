from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Any,
    Dict,
    List,
)

from docker.models.containers import Container

from tests.e2e.utilities.build_arg_configurations import BuildArgConfigurations
from tests.e2e.utilities.consts import (
    CommonMounts,
    ExpectedMount,
    ExpectedNamedVolume,
    MonorepoBuilderNamedVolumes,
    OT3FirmwareBuilderNamedVolumes,
    OT3FirmwareEmulatorNamedVolumesMap,
    OT3StateManagerNamedVolumes,
)
from tests.e2e.utilities.helper_functions import (
    get_mounts,
    get_volumes,
)
from tests.e2e.utilities.ot3_system import OT3System
from tests.e2e.utilities.ot3_system_test_messages import (
    E2ETestOutput,
    MONOREPO_BUILDER_CREATED,
    MONOREPO_BUILDER_NOT_CREATED,
    MONOREPO_SOURCE_MOUNTED,
    MONOREPO_SOURCE_NOT_MOUNTED,
    OPENTRONS_MODULES_BUILDER_CREATED,
    OPENTRONS_MODULES_BUILDER_NOT_CREATED,
    OPENTRONS_MODULES_SOURCE_MOUNTED,
    OPENTRONS_MODULES_SOURCE_NOT_MOUNTED,
    OT3_FIRMWARE_BUILDER_CREATED,
    OT3_FIRMWARE_BUILDER_NOT_CREATED,
    OT3_FIRMWARE_SOURCE_MOUNTED,
    OT3_FIRMWARE_SOURCE_NOT_MOUNTED,
    TestResult,
)


def _filter_mounts(
    container: Container, expected_mount: ExpectedMount
) -> List[Dict[str, Any]]:
    mounts = get_mounts(container)
    assert mounts is not None, "mounts are None"
    return [
        mount
        for mount in mounts
        if (
                mount["Type"] == "bind"
                and mount["Source"] == expected_mount.SOURCE_PATH
                and mount["Destination"] == expected_mount.DEST_PATH
        )
    ]


def _filter_volumes(
    container: Container, expected_vol: ExpectedNamedVolume
) -> List[Dict[str, Any]]:
    volumes = get_volumes(container)
    assert volumes is not None, "volumes are None"
    filtered_volume = [
        volume
        for volume in volumes
        if (
                volume["Type"] == "volume"
                and volume["Name"] == expected_vol.VOLUME_NAME
                and volume["Destination"] == expected_vol.DEST_PATH
        )
    ]

    return filtered_volume


def confirm_named_volume_exists(
    container: Container, expected_vol: ExpectedNamedVolume
) -> bool:
    return len(_filter_volumes(container, expected_vol)) == 1


def confirm_named_volume_does_not_exist(
    container: Container, expected_vol: ExpectedNamedVolume
) -> bool:
    return len(_filter_volumes(container, expected_vol)) == 0


def confirm_mount_exists(container: Container, expected_mount: ExpectedMount) -> bool:
    return len(_filter_mounts(container, expected_mount)) == 1


def confirm_mount_does_not_exist(
    container: Container, expected_mount: ExpectedMount
) -> bool:
    return len(_filter_mounts(container, expected_mount)) == 0


@dataclass
class OT3SystemTestDefinition:
    yaml_config_relative_path: str
    monorepo_builder_created: bool
    ot3_firmware_builder_created: bool
    opentrons_modules_builder_created: bool

    local_monorepo_mounted: bool
    local_ot3_firmware_mounted: bool
    local_opentrons_modules_mounted: bool

    monorepo_build_args: BuildArgConfigurations
    ot3_firmware_build_args: BuildArgConfigurations
    opentrons_modules_build_args: BuildArgConfigurations
    _test_output: E2ETestOutput = field(
        init=False,
        repr=False,
        compare=False,
        default=E2ETestOutput()
    )

    def _confirm_created_builders(self, ot3_system: OT3System) -> None:
        monorepo_builder_test_result: TestResult = (
            MONOREPO_BUILDER_CREATED
            if self.monorepo_builder_created
            else MONOREPO_BUILDER_NOT_CREATED
        )
        ot3_firmware_builder_test_result: TestResult = (
            OT3_FIRMWARE_BUILDER_CREATED
            if self.ot3_firmware_builder_created
            else OT3_FIRMWARE_BUILDER_NOT_CREATED
        )

        opentrons_modules_builder_test_result: TestResult = (
            OPENTRONS_MODULES_BUILDER_CREATED
            if self.opentrons_modules_builder_created
            else OPENTRONS_MODULES_BUILDER_NOT_CREATED
        )

        self._test_output.append_result(
            ot3_system.monorepo_builder_created == self.monorepo_builder_created,
            monorepo_builder_test_result
        )

        self._test_output.append_result(
            ot3_system.opentrons_modules_builder_created == self.opentrons_modules_builder_created,
            ot3_firmware_builder_test_result
        )
        self._test_output.append_result(
            ot3_system.opentrons_modules_builder_created
            == self.opentrons_modules_builder_created,
            opentrons_modules_builder_test_result
        )

    def _confirm_local_mounts(self, ot3_system: OT3System) -> None:
        monorepo_source_mounted_test_result: TestResult = (
            MONOREPO_SOURCE_MOUNTED
            if self.local_monorepo_mounted
            else MONOREPO_SOURCE_NOT_MOUNTED
        )
        ot3_firmware_source_mounted_test_result: TestResult = (
            OT3_FIRMWARE_SOURCE_MOUNTED
            if self.local_ot3_firmware_mounted
            else OT3_FIRMWARE_SOURCE_NOT_MOUNTED
        )

        opentrons_modules_source_mounted_test_result: TestResult = (
            OPENTRONS_MODULES_SOURCE_MOUNTED
            if self.local_opentrons_modules_mounted
            else OPENTRONS_MODULES_SOURCE_NOT_MOUNTED
        )

        self._test_output.append_result(
            ot3_system.local_monorepo_mounted == self.local_monorepo_mounted,
            monorepo_source_mounted_test_result
        )
        self._test_output.append_result(
            ot3_system.local_ot3_firmware_mounted == self.local_ot3_firmware_mounted,
            ot3_firmware_source_mounted_test_result
        )

        self._test_output.append_result(
            ot3_system.local_opentrons_modules_mounted == self.local_opentrons_modules_mounted,
            opentrons_modules_source_mounted_test_result
        )

    def _confirm_build_args(self, ot3_system: OT3System) -> None:
        monorepo_build_args_test_result = TestResult(
            desc=f"Confirming monorepo build args are: {self.monorepo_build_args.name}"
        )
        ot3_firmware_build_args_test_result = TestResult(
            desc=f"Confirming ot3-firmware build args are: {self.ot3_firmware_build_args.name}"
        )
        opentrons_modules_build_args_test_result = TestResult(
            desc=f"Confirming opentrons-modules build args are: {self.opentrons_modules_build_args.name}"
        )

        self._test_output.append_result(
            ot3_system.monorepo_build_args == self.monorepo_build_args,
            monorepo_build_args_test_result
        )
        self._test_output.append_result(
            ot3_system.ot3_firmware_build_args == self.ot3_firmware_build_args,
            ot3_firmware_build_args_test_result
        )
        self._test_output.append_result(
            ot3_system.opentrons_modules_build_args == self.opentrons_modules_build_args,
            opentrons_modules_build_args_test_result
        )

    def _confirm_ot3_emulator_named_volumes(self, ot3_system: OT3System) -> None:
        data = (
            (ot3_system.gantry_x, OT3FirmwareEmulatorNamedVolumesMap.GANTRY_X),
            (ot3_system.gantry_y, OT3FirmwareEmulatorNamedVolumesMap.GANTRY_Y),
            (ot3_system.head, OT3FirmwareEmulatorNamedVolumesMap.HEAD),
            (ot3_system.gripper, OT3FirmwareEmulatorNamedVolumesMap.GRIPPER),
            (ot3_system.pipettes, OT3FirmwareEmulatorNamedVolumesMap.PIPETTES),
            (ot3_system.bootloader, OT3FirmwareEmulatorNamedVolumesMap.BOOTLOADER),
        )
        for container, named_volume in data:
            test_result = TestResult.from_named_volume(container, named_volume)
            self._test_output.append_result(
                confirm_named_volume_exists(container, named_volume),
                test_result
            )

    def _confirm_entrypoint_mounts(self, ot3_system: OT3System) -> None:
        for container in ot3_system.containers_with_entrypoint_script:
            expected_mount = CommonMounts.ENTRYPOINT_MOUNT
            test_result = TestResult.from_mount(container, expected_mount)
            self._test_output.append_result(
                confirm_mount_exists(container, CommonMounts.ENTRYPOINT_MOUNT),
                test_result
            )

    def _confirm_ot3_firmware_builder_named_volumes(
        self,
        ot3_system: OT3System
    ) -> None:
        for volume in OT3FirmwareBuilderNamedVolumes.VOLUMES:
            test_result = TestResult.from_named_volume(
                ot3_system.firmware_builder,
                volume
            )
            self._test_output.append_result(
                confirm_named_volume_exists(ot3_system.firmware_builder, volume),
                test_result
            )

    def _confirm_ot3_firmware_state_manager_mounts_and_volumes(
        self,
        ot3_system: OT3System,
    ) -> None:
        for expected_volume in OT3StateManagerNamedVolumes.VOLUMES:
            test_result = TestResult.from_named_volume(
                ot3_system.state_manager,
                expected_volume
            )
            self._test_output.append_result(
                confirm_named_volume_exists(ot3_system.state_manager, expected_volume),
                test_result
            )

    def _confirm_containers_with_monorepo_wheel_volumes(
        self,
        ot3_system: OT3System
    ) -> None:
        for container in ot3_system.containers_with_monorepo_wheel_volume:
            for expected_volume in MonorepoBuilderNamedVolumes.VOLUMES:
                test_result = TestResult.from_named_volume(container, expected_volume)
                self._test_output.append_result(
                    confirm_named_volume_exists(container, expected_volume),
                    test_result
                )

    def compare(self, ot3_system: OT3System) -> None:
        self._confirm_created_builders(ot3_system)
        self._confirm_local_mounts(ot3_system)
        self._confirm_build_args(ot3_system)
        self._confirm_entrypoint_mounts(ot3_system)

        if self.monorepo_builder_created:
            test_result = TestResult.from_mount(
                ot3_system.monorepo_builder,
                CommonMounts.ENTRYPOINT_MOUNT,
                confirm_not_exists=True
            )
            self._test_output.append_result(
                confirm_mount_does_not_exist(
                    ot3_system.monorepo_builder, CommonMounts.ENTRYPOINT_MOUNT
                ),
                test_result
            )

            self._confirm_containers_with_monorepo_wheel_volumes(ot3_system)

        if self.ot3_firmware_builder_created:
            test_result = TestResult.from_mount(
                ot3_system.firmware_builder,
                CommonMounts.ENTRYPOINT_MOUNT,
                confirm_not_exists=True
            )
            self._test_output.append_result(
                confirm_mount_does_not_exist(
                    ot3_system.firmware_builder, CommonMounts.ENTRYPOINT_MOUNT
                ),
                test_result
            )

            self._confirm_ot3_emulator_named_volumes(ot3_system)
            self._confirm_ot3_firmware_builder_named_volumes(ot3_system)
            self._confirm_ot3_firmware_state_manager_mounts_and_volumes(ot3_system)

    def print_output(self) -> str:
        return self._test_output.get_results()
