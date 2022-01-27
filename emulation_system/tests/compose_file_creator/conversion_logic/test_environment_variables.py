"""Tests related to environment variables on services."""

import json
from typing import (
    Any,
    Dict,
    Type,
    cast,
)

import pytest

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


def test_robot_server_emulator_proxy_env_vars_added(
    robot_with_mount_and_modules_services: Dict[str, Any]
) -> None:
    """Confirm env vars are set correctly."""
    env = robot_with_mount_and_modules_services[OT2_ID].environment
    assert env is not None
    assert "OT_SMOOTHIE_EMULATOR_URI" in env.__root__
    assert env.__root__["OT_SMOOTHIE_EMULATOR_URI"] == f"socket://{SMOOTHIE_ID}:11000"
    assert "OT_EMULATOR_module_server" in env.__root__
    assert (
        env.__root__["OT_EMULATOR_module_server"]
        == f'{{"host": "{EMULATOR_PROXY_ID}"}}'
    )


def test_robot_server_emulator_proxy_env_vars_not_added(
    ot2_only: Dict[str, Any]
) -> None:
    """Confirm that env vars are not added to robot server when there are no modules."""
    robot_services = convert_from_obj(ot2_only).services
    assert robot_services is not None
    robot_services_env = robot_services[OT2_ID].environment
    assert robot_services_env is not None
    assert "OT_EMULATOR_module_server" not in robot_services_env.__root__


def test_ot3_feature_flag_added(ot3_only: Dict[str, Any]) -> None:
    """Confirm feature flag is added when robot is an OT3."""
    robot_services = convert_from_obj(ot3_only).services
    assert robot_services is not None
    env = robot_services[OT3_ID].environment
    assert env is not None
    assert "OT_API_FF_enableOT3HardwareController" in env.__root__
    root = cast(Dict[str, str], env.__root__)
    assert root["OT_API_FF_enableOT3HardwareController"] == "True"


@pytest.mark.parametrize(
    "service_name,input_class",
    [
        [TEMPERATURE_MODULE_ID, TemperatureModuleInputModel],
        [MAGNETIC_MODULE_ID, MagneticModuleInputModel],
    ],
)
def test_firmware_serial_number_env_vars(
    service_name: str,
    input_class: Type[ModuleInputModel],
    robot_with_mount_and_modules_services: Dict[str, Service],
) -> None:
    """Confirm that serial number env vars are created correctly on firmware modules."""
    services = robot_with_mount_and_modules_services
    assert services is not None

    module_env = services[service_name].environment
    assert module_env is not None
    assert input_class.firmware_serial_number_info is not None
    assert input_class.firmware_serial_number_info.env_var_name in module_env.__root__

    module_root = cast(Dict[str, str], module_env.__root__)
    assert module_root[
        input_class.firmware_serial_number_info.env_var_name
    ] == json.dumps(
        {
            "serial_number": service_name,
            "model": input_class.firmware_serial_number_info.model,
            "version": input_class.firmware_serial_number_info.version,
        }
    )


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


def test_smoothie_pipettes(ot2_only: Dict[str, Any]) -> None:
    """Confirm that pipettes JSON is added to smoothie Service."""
    services = convert_from_obj(ot2_only).services
    assert services is not None
    smoothie_env = services[SMOOTHIE_ID].environment
    assert smoothie_env is not None
    assert "OT_EMULATOR_smoothie" in smoothie_env.__root__


def test_pipettes_not_added_to_robot_server(ot2_only: Dict[str, Any]) -> None:
    """Confirm that pipettes JSON is not added to OT2(robot-server) service."""
    services = convert_from_obj(ot2_only).services
    assert services is not None
    ot2_env = services[OT2_ID].environment
    assert ot2_env is not None
    assert "OT_EMULATOR_smoothie" not in ot2_env.__root__
