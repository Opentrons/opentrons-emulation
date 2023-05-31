"""Tests for the creation of services not directly defined in input file.

These will be emulation-proxy, smoothie, and ot3 firmware services
Tests for checking env variables, such as pipettes for smoothie, are in
test_environment_variables.py
"""

from typing import Any, Dict

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator.config_file_settings import OT3Hardware
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.images import (
    OT3BootloaderImage,
    OT3GantryXImage,
    OT3GantryYImage,
    OT3GripperImage,
    OT3HeadImage,
    OT3PipettesImage,
    SmoothieImage,
)
from tests.conftest import EMULATOR_PROXY_ID
from tests.validation_helper_functions import partial_string_in_mount


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_remote_everything_commit_id"),
        lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"),
        lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"),
        lazy_fixture("ot3_and_modules"),
        lazy_fixture("modules_only"),
        lazy_fixture("heater_shaker_module_hardware_remote"),
        lazy_fixture("heater_shaker_module_hardware_local"),
        lazy_fixture("heater_shaker_module_firmware_local"),
        lazy_fixture("heater_shaker_module_firmware_remote"),
        lazy_fixture("thermocycler_module_hardware_local"),
        lazy_fixture("thermocycler_module_firmware_local"),
        lazy_fixture("thermocycler_module_hardware_remote"),
        lazy_fixture("thermocycler_module_firmware_remote"),
        lazy_fixture("temperature_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_local"),
        lazy_fixture("ot2_only"),
        lazy_fixture("ot2_and_modules"),
        lazy_fixture("ot2_remote_everything_commit_id"),
        lazy_fixture("ot2_local_source"),
    ],
)
def test_emulation_proxy_created(
    config: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Verify emulator proxy is created when there are modules."""
    services = convert_from_obj(config, testing_global_em_config, False).services
    assert services is not None
    assert EMULATOR_PROXY_ID in set(services.keys())


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_only"),
        lazy_fixture("ot2_and_modules"),
        lazy_fixture("ot2_remote_everything_commit_id"),
        lazy_fixture("ot2_local_source"),
    ],
)
def test_smoothie_created(
    config: Dict[str, Any],
    opentrons_dir: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm smoothie uses local source when OT2 is set to local and has mounts."""
    runtime_compose_file_model = convert_from_obj(
        config, testing_global_em_config, False
    )
    smoothie = runtime_compose_file_model.smoothie_emulator
    assert smoothie is not None
    assert smoothie.image == SmoothieImage().image_name


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot3_remote_everything_commit_id"),
        lazy_fixture("ot3_local_ot3_firmware_remote_monorepo"),
        lazy_fixture("ot3_remote_ot3_firmware_local_monorepo"),
        lazy_fixture("ot3_and_modules"),
        lazy_fixture("modules_only"),
        lazy_fixture("heater_shaker_module_hardware_remote"),
        lazy_fixture("heater_shaker_module_hardware_local"),
        lazy_fixture("heater_shaker_module_firmware_local"),
        lazy_fixture("heater_shaker_module_firmware_remote"),
        lazy_fixture("thermocycler_module_hardware_local"),
        lazy_fixture("thermocycler_module_firmware_local"),
        lazy_fixture("thermocycler_module_hardware_remote"),
        lazy_fixture("thermocycler_module_firmware_remote"),
        lazy_fixture("temperature_module_firmware_local"),
        lazy_fixture("temperature_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_remote"),
        lazy_fixture("magnetic_module_firmware_local"),
    ],
)
def test_smoothie_not_created(
    config: Dict[str, Any],
    opentrons_dir: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm smoothie uses local source when OT2 is set to local and has mounts."""
    runtime_compose_file_model = convert_from_obj(
        config, testing_global_em_config, False
    )
    smoothie = runtime_compose_file_model.smoothie_emulator
    assert smoothie is None


@pytest.mark.parametrize(
    "container_name, expected_image_name",
    [
        [OT3Hardware.LEFT_PIPETTE.value, OT3PipettesImage().image_name],
        [OT3Hardware.HEAD.value, OT3HeadImage().image_name],
        [OT3Hardware.GANTRY_X.value, OT3GantryXImage().image_name],
        [OT3Hardware.GANTRY_Y.value, OT3GantryYImage().image_name],
        [OT3Hardware.BOOTLOADER.value, OT3BootloaderImage().image_name],
        [OT3Hardware.GRIPPER.value, OT3GripperImage().image_name],
    ],
)
def test_local_ot3_services_created(
    container_name: str,
    expected_image_name: str,
    ot3_only: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm OT3 hardware emulators are added with OT3 is specified."""
    services = convert_from_obj(ot3_only, testing_global_em_config, False).services
    assert services is not None
    assert container_name in list(services.keys())

    service = services[container_name]
    assert service.image == expected_image_name

    partial_string_in_mount("entrypoint.sh:/entrypoint.sh", service)
    partial_string_in_mount("ot3-firmware:/ot3-firmware", service)
