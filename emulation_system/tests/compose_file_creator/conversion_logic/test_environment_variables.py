"""Tests related to environment variables on services."""

import json
from typing import (
    Any,
    Dict,
    Type,
    cast,
)

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    ModuleInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import Service
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from tests.compose_file_creator.conftest import (
    EMULATOR_PROXY_ID,
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    OT3_ID,
    SMOOTHIE_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)


@pytest.mark.parametrize(
    "config", [lazy_fixture("robot_with_mount_and_modules"), lazy_fixture("ot2_only")]
)
def test_robot_server_emulator_proxy_env_vars_added(
    config: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm env vars are set correctly."""
    services = convert_from_obj(config, testing_global_em_config).services
    assert services is not None
    env = services[OT2_ID].environment
    assert env is not None
    env_root = cast(Dict[str, Any], env.__root__)

    assert env_root is not None
    assert "OT_SMOOTHIE_EMULATOR_URI" in env_root
    assert env_root["OT_SMOOTHIE_EMULATOR_URI"] == f"socket://{SMOOTHIE_ID}:11000"
    assert "OT_EMULATOR_module_server" in env_root
    assert env_root["OT_EMULATOR_module_server"] == f'{{"host": "{EMULATOR_PROXY_ID}"}}'


def test_ot3_feature_flag_added(
    ot3_only: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Confirm feature flag is added when robot is an OT3."""
    robot_services = convert_from_obj(ot3_only, testing_global_em_config).services
    assert robot_services is not None
    env = robot_services[OT3_ID].environment
    assert env is not None
    assert "OT_API_FF_enableOT3HardwareController" in env.__root__
    root = cast(Dict[str, str], env.__root__)
    assert root["OT_API_FF_enableOT3HardwareController"] == "True"


@pytest.mark.parametrize(
    "model,input_class,expected_value",
    [
        [
            lazy_fixture("temperature_module_default"),
            TemperatureModuleInputModel,
            {
                "serial_number": "temperamental",
                "model": "temp_deck_v20",
                "version": "v2.0.1",
                "temperature": {"degrees_per_tick": 2.0, "starting": 23.0},
            },
        ],
        [
            lazy_fixture("magnetic_module_default"),
            MagneticModuleInputModel,
            {
                "serial_number": "fatal-attraction",
                "model": "mag_deck_v20",
                "version": "2.0.0",
            },
        ],
        [
            lazy_fixture("thermocycler_module_firmware_emulation_level"),
            ThermocyclerModuleInputModel,
            {
                "serial_number": "t00-hot-to-handle",
                "model": "v02",
                "version": "v1.1.0",
                "lid_temperature": {"degrees_per_tick": 2.0, "starting": 23.0},
                "plate_temperature": {"degrees_per_tick": 2.0, "starting": 23.0},
            },
        ],
    ],
)
def test_firmware_serial_number_env_vars(
    model: Dict[str, Any],
    input_class: Type[ModuleInputModel],
    expected_value: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that serial number env vars are created correctly on firmware modules."""
    services = convert_from_obj({"modules": [model]}, testing_global_em_config).services
    assert services is not None

    module_env = services[model["id"]].environment
    assert module_env is not None
    assert input_class.firmware_serial_number_info is not None
    assert input_class.firmware_serial_number_info.env_var_name in module_env.__root__

    module_root = cast(Dict[str, str], module_env.__root__)
    assert module_root[
        input_class.firmware_serial_number_info.env_var_name
    ] == json.dumps(expected_value)


@pytest.mark.parametrize(
    "service_name",
    [
        THERMOCYCLER_MODULE_ID,
        HEATER_SHAKER_MODULE_ID,
    ],
)
def test_hardware_serial_number_env_vars(
    service_name: str, robot_with_mount_and_modules_services: Dict[str, Service]
) -> None:
    """Confirm that serial number env vars are created correctly on hardware modules."""
    services = robot_with_mount_and_modules_services
    assert services is not None

    module_env = services[service_name].environment
    assert module_env is not None
    assert "SERIAL_NUMBER" in module_env.__root__

    module_root = cast(Dict[str, str], module_env.__root__)
    assert module_root["SERIAL_NUMBER"] == service_name


@pytest.mark.parametrize(
    "service_name, input_class",
    [
        [TEMPERATURE_MODULE_ID, TemperatureModuleInputModel],
        [THERMOCYCLER_MODULE_ID, ThermocyclerModuleInputModel],
        [HEATER_SHAKER_MODULE_ID, HeaterShakerModuleInputModel],
        [MAGNETIC_MODULE_ID, MagneticModuleInputModel],
    ],
)
def test_em_proxy_info_env_vars_on_modules(
    service_name: str,
    input_class: Type[ModuleInputModel],
    robot_with_mount_and_modules_services: Dict[str, Service],
) -> None:
    """Confirm that serial number env vars are created correctly on hardware modules."""
    services = robot_with_mount_and_modules_services
    assert services is not None

    module_env = services[service_name].environment
    assert module_env is not None
    assert input_class.proxy_info.env_var_name in module_env.__root__

    module_root = cast(Dict[str, str], module_env.__root__)
    assert module_root[input_class.proxy_info.env_var_name] == json.dumps(
        {
            "emulator_port": input_class.proxy_info.emulator_port,
            "driver_port": input_class.proxy_info.driver_port,
        }
    )


@pytest.mark.parametrize(
    "input_class",
    [
        TemperatureModuleInputModel,
        ThermocyclerModuleInputModel,
        HeaterShakerModuleInputModel,
        MagneticModuleInputModel,
    ],
)
def test_em_proxy_info_env_vars_on_proxy(
    input_class: Type[ModuleInputModel],
    robot_with_mount_and_modules_services: Dict[str, Service],
) -> None:
    """Confirm that serial number env vars are created correctly on emulator proxy."""
    services = robot_with_mount_and_modules_services
    assert services is not None

    emulator_proxy_env = services[EMULATOR_PROXY_ID].environment
    assert emulator_proxy_env is not None
    assert input_class.proxy_info.env_var_name in emulator_proxy_env.__root__

    module_root = cast(Dict[str, str], emulator_proxy_env.__root__)
    assert module_root[input_class.proxy_info.env_var_name] == json.dumps(
        {
            "emulator_port": input_class.proxy_info.emulator_port,
            "driver_port": input_class.proxy_info.driver_port,
        }
    )


def test_smoothie_pipettes(
    ot2_only: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Confirm that pipettes JSON is added to smoothie Service."""
    services = convert_from_obj(ot2_only, testing_global_em_config).services
    assert services is not None
    smoothie_env = services[SMOOTHIE_ID].environment
    assert smoothie_env is not None
    assert "OT_EMULATOR_smoothie" in smoothie_env.__root__


def test_pipettes_not_added_to_robot_server(
    ot2_only: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Confirm that pipettes JSON is not added to OT2(robot-server) service."""
    services = convert_from_obj(ot2_only, testing_global_em_config).services
    assert services is not None
    ot2_env = services[OT2_ID].environment
    assert ot2_env is not None
    assert "OT_EMULATOR_smoothie" not in ot2_env.__root__
