"""Confirm that custom env vars are added to services correctly."""

from typing import Any, Dict, cast

import pytest
from validation_helper_functions import get_env

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
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

OT2_ROBOT_SERVER_VAL_1 = "ot2"
OT2_ROBOT_SERVER_VAL_2 = 1
OT2_ROBOT_SERVER_VAL_3 = 1.1

SMOOTHIE_VAL_1 = "smoothie"
SMOOTHIE_VAL_2 = 2
SMOOTHIE_VAL_3 = 2.2

OT2_EM_PROXY_VAL_1 = "ot2 emulator proxy"
OT2_EM_PROXY_VAL_2 = 3
OT2_EM_PROXY_VAL_3 = 3.3

HS_VAL_1 = "heater shaker module"
HS_VAL_2 = 4
HS_VAL_3 = 4.4

THERM_VAL_1 = "thermocycler module"
THERM_VAL_2 = 5
THERM_VAL_3 = 5.5

TEMP_VAL_1 = "temperature module"
TEMP_VAL_2 = 6
TEMP_VAL_3 = 6.6

MAG_VAL_1 = "magnetic module"
MAG_VAL_2 = 7
MAG_VAL_3 = 7.7

OT3_ROBOT_SERVER_VAL_1 = "ot3"
OT3_ROBOT_SERVER_VAL_2 = 8
OT3_ROBOT_SERVER_VAL_3 = 8.8

OT3_EM_PROXY_VAL_1 = "ot3 emulator proxy"
OT3_EM_PROXY_VAL_2 = 9
OT3_EM_PROXY_VAL_3 = 9.9

OT3_PIPETTES_VAL_1 = "ot3 pipettes"
OT3_PIPETTES_VAL_2 = 10
OT3_PIPETTES_VAL_3 = 10.10

OT3_GRIPPER_VAL_1 = "ot3 gripper"
OT3_GRIPPER_VAL_2 = 11
OT3_GRIPPER_VAL_3 = 11.11

OT3_HEAD_VAL_1 = "ot3 head"
OT3_HEAD_VAL_2 = 12
OT3_HEAD_VAL_3 = 12.12

OT3_GANTRY_X_VAL_1 = "ot3 gantry x"
OT3_GANTRY_X_VAL_2 = 13
OT3_GANTRY_X_VAL_3 = 13.13

OT3_GANTRY_Y_VAL_1 = "ot3 gantry y"
OT3_GANTRY_Y_VAL_2 = 14
OT3_GANTRY_Y_VAL_3 = 14.14

OT3_BOOTLOADER_VAL_1 = "ot3 bootloader"
OT3_BOOTLOADER_VAL_2 = 15
OT3_BOOTLOADER_VAL_3 = 15.15

OT3_CAN_SERVER_VAL_1 = "ot3 can server"
OT3_CAN_SERVER_VAL_2 = 16
OT3_CAN_SERVER_VAL_3 = 16.16


@pytest.fixture
def ot2_with_custom_env_vars(
    ot2_only: Dict[str, Any],
    heater_shaker_model: Dict[str, Any],
    thermocycler_model: Dict[str, Any],
    temperature_model: Dict[str, Any],
    magdeck_model: Dict[str, Any],
) -> Dict[str, Any]:
    """Create an OT2 configuration with custom env vars.

    Custom env vars for robot server, smoothie, emulator proxy, temperature module
    magnetic module, thermocycler module, and heater shaker module.
    """
    ot2_only["robot"]["robot-server-env-vars"] = {}
    robot_server_env_vars = ot2_only["robot"]["robot-server-env-vars"]
    robot_server_env_vars["robot-server-1"] = OT2_ROBOT_SERVER_VAL_1
    robot_server_env_vars["robot-server-2"] = OT2_ROBOT_SERVER_VAL_2
    robot_server_env_vars["robot-server-3"] = OT2_ROBOT_SERVER_VAL_3

    ot2_only["robot"]["smoothie-env-vars"] = {}
    smoothie_env_vars = ot2_only["robot"]["smoothie-env-vars"]
    smoothie_env_vars["smoothie-1"] = SMOOTHIE_VAL_1
    smoothie_env_vars["smoothie-2"] = SMOOTHIE_VAL_2
    smoothie_env_vars["smoothie-3"] = SMOOTHIE_VAL_3

    ot2_only["robot"]["emulator-proxy-env-vars"] = {}
    emulator_proxy_env_vars = ot2_only["robot"]["emulator-proxy-env-vars"]
    emulator_proxy_env_vars["emulator-proxy-1"] = OT2_EM_PROXY_VAL_1
    emulator_proxy_env_vars["emulator-proxy-2"] = OT2_EM_PROXY_VAL_2
    emulator_proxy_env_vars["emulator-proxy-3"] = OT2_EM_PROXY_VAL_3

    heater_shaker_model["module-env-vars"] = {}
    hs_env_vars = heater_shaker_model["module-env-vars"]
    hs_env_vars["heater-shaker-1"] = HS_VAL_1
    hs_env_vars["heater-shaker-2"] = HS_VAL_2
    hs_env_vars["heater-shaker-3"] = HS_VAL_3

    thermocycler_model["module-env-vars"] = {}
    therm_env_vars = thermocycler_model["module-env-vars"]
    therm_env_vars["therm-1"] = THERM_VAL_1
    therm_env_vars["therm-2"] = THERM_VAL_2
    therm_env_vars["therm-3"] = THERM_VAL_3

    temperature_model["module-env-vars"] = {}
    temp_env_vars = temperature_model["module-env-vars"]
    temp_env_vars["temp-1"] = TEMP_VAL_1
    temp_env_vars["temp-2"] = TEMP_VAL_2
    temp_env_vars["temp-3"] = TEMP_VAL_3

    magdeck_model["module-env-vars"] = {}
    mag_env_vars = magdeck_model["module-env-vars"]
    mag_env_vars["mag-1"] = MAG_VAL_1
    mag_env_vars["mag-2"] = MAG_VAL_2
    mag_env_vars["mag-3"] = MAG_VAL_3

    ot2_only["modules"] = []
    ot2_only["modules"].extend(
        [
            heater_shaker_model,
            thermocycler_model,
            temperature_model,
            magdeck_model,
        ]
    )

    return ot2_only


@pytest.fixture
def ot3_with_custom_env_vars(ot3_only: Dict[str, Any]) -> Dict[str, Any]:
    """Create an OT3 configuration with custom env vars.

    Custom env vars for robot server, can server, emulator proxy, gripper, head
    bootloader, pipettes, gantry x, and gantry y.
    """
    ot3_only["robot"]["robot-server-env-vars"] = {}
    robot_server_env_vars = ot3_only["robot"]["robot-server-env-vars"]
    robot_server_env_vars["robot-server-1"] = OT3_ROBOT_SERVER_VAL_1
    robot_server_env_vars["robot-server-2"] = OT3_ROBOT_SERVER_VAL_2
    robot_server_env_vars["robot-server-3"] = OT3_ROBOT_SERVER_VAL_3

    ot3_only["robot"]["emulator-proxy-env-vars"] = {}
    emulator_proxy_env_vars = ot3_only["robot"]["emulator-proxy-env-vars"]
    emulator_proxy_env_vars["emulator-proxy-1"] = OT3_EM_PROXY_VAL_1
    emulator_proxy_env_vars["emulator-proxy-2"] = OT3_EM_PROXY_VAL_2
    emulator_proxy_env_vars["emulator-proxy-3"] = OT3_EM_PROXY_VAL_3

    ot3_only["robot"]["pipettes-env-vars"] = {}
    pipettes_env_vars = ot3_only["robot"]["pipettes-env-vars"]
    pipettes_env_vars["pipettes-1"] = OT3_PIPETTES_VAL_1
    pipettes_env_vars["pipettes-2"] = OT3_PIPETTES_VAL_2
    pipettes_env_vars["pipettes-3"] = OT3_PIPETTES_VAL_3

    ot3_only["robot"]["gripper-env-vars"] = {}
    gripper_env_vars = ot3_only["robot"]["gripper-env-vars"]
    gripper_env_vars["gripper-1"] = OT3_GRIPPER_VAL_1
    gripper_env_vars["gripper-2"] = OT3_GRIPPER_VAL_2
    gripper_env_vars["gripper-3"] = OT3_GRIPPER_VAL_3

    ot3_only["robot"]["head-env-vars"] = {}
    head_env_vars = ot3_only["robot"]["head-env-vars"]
    head_env_vars["head-1"] = OT3_HEAD_VAL_1
    head_env_vars["head-2"] = OT3_HEAD_VAL_2
    head_env_vars["head-3"] = OT3_HEAD_VAL_3

    ot3_only["robot"]["gantry-x-env-vars"] = {}
    gantry_x_vars = ot3_only["robot"]["gantry-x-env-vars"]
    gantry_x_vars["gantry-x-1"] = OT3_GANTRY_X_VAL_1
    gantry_x_vars["gantry-x-2"] = OT3_GANTRY_X_VAL_2
    gantry_x_vars["gantry-x-3"] = OT3_GANTRY_X_VAL_3

    ot3_only["robot"]["gantry-y-env-vars"] = {}
    gantry_y_vars = ot3_only["robot"]["gantry-y-env-vars"]
    gantry_y_vars["gantry-y-1"] = OT3_GANTRY_Y_VAL_1
    gantry_y_vars["gantry-y-2"] = OT3_GANTRY_Y_VAL_2
    gantry_y_vars["gantry-y-3"] = OT3_GANTRY_Y_VAL_3

    ot3_only["robot"]["bootloader-env-vars"] = {}
    bootloader_vars = ot3_only["robot"]["bootloader-env-vars"]
    bootloader_vars["bootloader-1"] = OT3_BOOTLOADER_VAL_1
    bootloader_vars["bootloader-2"] = OT3_BOOTLOADER_VAL_2
    bootloader_vars["bootloader-3"] = OT3_BOOTLOADER_VAL_3

    ot3_only["robot"]["can-server-env-vars"] = {}
    can_server_vars = ot3_only["robot"]["can-server-env-vars"]
    can_server_vars["can-server-1"] = OT3_CAN_SERVER_VAL_1
    can_server_vars["can-server-2"] = OT3_CAN_SERVER_VAL_2
    can_server_vars["can-server-3"] = OT3_CAN_SERVER_VAL_3

    return ot3_only


def test_ot2_env_vars(
    ot2_with_custom_env_vars: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm custom env vars are created.

    Custom env vars for robot server, smoothie, emulator proxy, temperature module
    magnetic module, thermocycler module, and heater shaker module.
    """
    services = convert_from_obj(
        ot2_with_custom_env_vars, testing_global_em_config, dev=False
    ).services

    assert services is not None
    robot_server = services[OT2_ID]
    emulator_proxy = services[EMULATOR_PROXY_ID]
    smoothie = services[SMOOTHIE_ID]
    heater_shaker_module = services[f"{HEATER_SHAKER_MODULE_ID}-1"]
    magnetic_module = services[f"{MAGNETIC_MODULE_ID}-1"]
    temperature_module = services[f"{TEMPERATURE_MODULE_ID}-1"]
    thermocycler_module = services[f"{THERMOCYCLER_MODULE_ID}-1"]

    assert robot_server is not None
    assert emulator_proxy is not None
    assert smoothie is not None
    assert heater_shaker_module is not None
    assert magnetic_module is not None
    assert temperature_module is not None
    assert thermocycler_module is not None

    assert robot_server.environment is not None
    assert emulator_proxy.environment is not None
    assert smoothie.environment is not None
    assert heater_shaker_module.environment is not None
    assert magnetic_module.environment is not None
    assert temperature_module.environment is not None
    assert thermocycler_module.environment is not None

    # environment will only ever be a Dict due to implementation
    # so cast it
    robot_server_env = get_env(robot_server)
    emulator_proxy_env = get_env(emulator_proxy)
    smoothie_env = get_env(smoothie)
    heater_shaker_module_env = get_env(heater_shaker_module)
    magnetic_module_env = get_env(magnetic_module)
    temperature_module_env = get_env(temperature_module)
    thermocycler_module_env = get_env(thermocycler_module)

    assert robot_server_env is not None
    assert emulator_proxy_env is not None
    assert smoothie_env is not None
    assert heater_shaker_module_env is not None
    assert magnetic_module_env is not None
    assert temperature_module_env is not None
    assert thermocycler_module_env is not None

    assert "robot-server-1" in robot_server_env.keys()
    assert "robot-server-2" in robot_server_env.keys()
    assert "robot-server-3" in robot_server_env.keys()
    assert robot_server_env["robot-server-1"] == str(OT2_ROBOT_SERVER_VAL_1)
    assert robot_server_env["robot-server-2"] == str(OT2_ROBOT_SERVER_VAL_2)
    assert robot_server_env["robot-server-3"] == str(OT2_ROBOT_SERVER_VAL_3)

    assert "smoothie-1" in smoothie_env.keys()
    assert "smoothie-2" in smoothie_env.keys()
    assert "smoothie-3" in smoothie_env.keys()
    assert smoothie_env["smoothie-1"] == str(SMOOTHIE_VAL_1)
    assert smoothie_env["smoothie-2"] == str(SMOOTHIE_VAL_2)
    assert smoothie_env["smoothie-3"] == str(SMOOTHIE_VAL_3)

    assert "emulator-proxy-1" in emulator_proxy_env.keys()
    assert "emulator-proxy-2" in emulator_proxy_env.keys()
    assert "emulator-proxy-3" in emulator_proxy_env.keys()
    assert emulator_proxy_env["emulator-proxy-1"] == str(OT2_EM_PROXY_VAL_1)
    assert emulator_proxy_env["emulator-proxy-2"] == str(OT2_EM_PROXY_VAL_2)
    assert emulator_proxy_env["emulator-proxy-3"] == str(OT2_EM_PROXY_VAL_3)

    assert "heater-shaker-1" in heater_shaker_module_env.keys()
    assert "heater-shaker-2" in heater_shaker_module_env.keys()
    assert "heater-shaker-3" in heater_shaker_module_env.keys()
    assert heater_shaker_module_env["heater-shaker-1"] == str(HS_VAL_1)
    assert heater_shaker_module_env["heater-shaker-2"] == str(HS_VAL_2)
    assert heater_shaker_module_env["heater-shaker-3"] == str(HS_VAL_3)

    assert "therm-1" in thermocycler_module_env.keys()
    assert "therm-2" in thermocycler_module_env.keys()
    assert "therm-3" in thermocycler_module_env.keys()
    assert thermocycler_module_env["therm-1"] == str(THERM_VAL_1)
    assert thermocycler_module_env["therm-2"] == str(THERM_VAL_2)
    assert thermocycler_module_env["therm-3"] == str(THERM_VAL_3)

    assert "temp-1" in temperature_module_env.keys()
    assert "temp-2" in temperature_module_env.keys()
    assert "temp-3" in temperature_module_env.keys()
    assert temperature_module_env["temp-1"] == str(TEMP_VAL_1)
    assert temperature_module_env["temp-2"] == str(TEMP_VAL_2)
    assert temperature_module_env["temp-3"] == str(TEMP_VAL_3)

    assert "mag-1" in magnetic_module_env.keys()
    assert "mag-2" in magnetic_module_env.keys()
    assert "mag-3" in magnetic_module_env.keys()
    assert magnetic_module_env["mag-1"] == str(MAG_VAL_1)
    assert magnetic_module_env["mag-2"] == str(MAG_VAL_2)
    assert magnetic_module_env["mag-3"] == str(MAG_VAL_3)


def test_ot3_env_vars(
    ot3_with_custom_env_vars: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm custom env vars are created.

    Custom env vars for robot server, can-server, emulator proxy, gripper, head
    pipettes, gantry x, gantry y, and bootloader.
    """
    services = convert_from_obj(
        ot3_with_custom_env_vars, testing_global_em_config, dev=False
    ).services
    assert services is not None

    robot_server = services[OT3_ID]
    emulator_proxy = services[EMULATOR_PROXY_ID]
    can_server = services["can-server"]
    head = services["ot3-head"]
    pipettes = services["ot3-pipettes"]
    gantry_x = services["ot3-gantry-x"]
    gantry_y = services["ot3-gantry-y"]
    bootloader = services["ot3-bootloader"]
    gripper = services["ot3-gripper"]

    assert robot_server is not None
    assert emulator_proxy is not None
    assert can_server is not None
    assert head is not None
    assert pipettes is not None
    assert gantry_x is not None
    assert gantry_y is not None
    assert bootloader is not None
    assert gripper is not None

    assert robot_server.environment is not None
    assert emulator_proxy.environment is not None
    assert can_server.environment is not None
    assert head.environment is not None
    assert pipettes.environment is not None
    assert gantry_x.environment is not None
    assert gantry_y.environment is not None
    assert bootloader.environment is not None
    assert gripper.environment is not None

    # environment will only ever be a Dict due to implementation
    # so cast it
    robot_server_env = cast(Dict, robot_server.environment.__root__)
    emulator_proxy_env = cast(Dict, emulator_proxy.environment.__root__)
    can_server_env = cast(Dict, can_server.environment.__root__)
    head_env = cast(Dict, head.environment.__root__)
    pipettes_env = cast(Dict, pipettes.environment.__root__)
    gantry_x_env = cast(Dict, gantry_x.environment.__root__)
    gantry_y_env = cast(Dict, gantry_y.environment.__root__)
    bootloader_env = cast(Dict, bootloader.environment.__root__)
    gripper_env = cast(Dict, gripper.environment.__root__)

    assert robot_server_env is not None
    assert emulator_proxy_env is not None
    assert can_server_env is not None
    assert head_env is not None
    assert pipettes_env is not None
    assert gantry_x_env is not None
    assert gantry_y_env is not None
    assert bootloader_env is not None
    assert gripper_env is not None

    assert "robot-server-1" in robot_server_env.keys()
    assert "robot-server-2" in robot_server_env.keys()
    assert "robot-server-3" in robot_server_env.keys()
    assert robot_server_env["robot-server-1"] == str(OT3_ROBOT_SERVER_VAL_1)
    assert robot_server_env["robot-server-2"] == str(OT3_ROBOT_SERVER_VAL_2)
    assert robot_server_env["robot-server-3"] == str(OT3_ROBOT_SERVER_VAL_3)

    assert "emulator-proxy-1" in emulator_proxy_env.keys()
    assert "emulator-proxy-2" in emulator_proxy_env.keys()
    assert "emulator-proxy-3" in emulator_proxy_env.keys()
    assert emulator_proxy_env["emulator-proxy-1"] == str(OT3_EM_PROXY_VAL_1)
    assert emulator_proxy_env["emulator-proxy-2"] == str(OT3_EM_PROXY_VAL_2)
    assert emulator_proxy_env["emulator-proxy-3"] == str(OT3_EM_PROXY_VAL_3)

    assert "can-server-1" in can_server_env.keys()
    assert "can-server-2" in can_server_env.keys()
    assert "can-server-3" in can_server_env.keys()
    assert can_server_env["can-server-1"] == str(OT3_CAN_SERVER_VAL_1)
    assert can_server_env["can-server-2"] == str(OT3_CAN_SERVER_VAL_2)
    assert can_server_env["can-server-3"] == str(OT3_CAN_SERVER_VAL_3)

    assert "pipettes-1" in pipettes_env.keys()
    assert "pipettes-2" in pipettes_env.keys()
    assert "pipettes-3" in pipettes_env.keys()
    assert pipettes_env["pipettes-1"] == str(OT3_PIPETTES_VAL_1)
    assert pipettes_env["pipettes-2"] == str(OT3_PIPETTES_VAL_2)
    assert pipettes_env["pipettes-3"] == str(OT3_PIPETTES_VAL_3)

    assert "gripper-1" in gripper_env.keys()
    assert "gripper-2" in gripper_env.keys()
    assert "gripper-3" in gripper_env.keys()
    assert gripper_env["gripper-1"] == str(OT3_GRIPPER_VAL_1)
    assert gripper_env["gripper-2"] == str(OT3_GRIPPER_VAL_2)
    assert gripper_env["gripper-3"] == str(OT3_GRIPPER_VAL_3)

    assert "head-1" in head_env.keys()
    assert "head-2" in head_env.keys()
    assert "head-3" in head_env.keys()
    assert head_env["head-1"] == str(OT3_HEAD_VAL_1)
    assert head_env["head-2"] == str(OT3_HEAD_VAL_2)
    assert head_env["head-3"] == str(OT3_HEAD_VAL_3)

    assert "bootloader-1" in bootloader_env.keys()
    assert "bootloader-2" in bootloader_env.keys()
    assert "bootloader-3" in bootloader_env.keys()
    assert bootloader_env["bootloader-1"] == str(OT3_BOOTLOADER_VAL_1)
    assert bootloader_env["bootloader-2"] == str(OT3_BOOTLOADER_VAL_2)
    assert bootloader_env["bootloader-3"] == str(OT3_BOOTLOADER_VAL_3)

    assert "gantry-x-1" in gantry_x_env.keys()
    assert "gantry-x-2" in gantry_x_env.keys()
    assert "gantry-x-3" in gantry_x_env.keys()
    assert gantry_x_env["gantry-x-1"] == str(OT3_GANTRY_X_VAL_1)
    assert gantry_x_env["gantry-x-2"] == str(OT3_GANTRY_X_VAL_2)
    assert gantry_x_env["gantry-x-3"] == str(OT3_GANTRY_X_VAL_3)

    assert "gantry-y-1" in gantry_y_env.keys()
    assert "gantry-y-2" in gantry_y_env.keys()
    assert "gantry-y-3" in gantry_y_env.keys()
    assert gantry_y_env["gantry-y-1"] == str(OT3_GANTRY_Y_VAL_1)
    assert gantry_y_env["gantry-y-2"] == str(OT3_GANTRY_Y_VAL_2)
    assert gantry_y_env["gantry-y-3"] == str(OT3_GANTRY_Y_VAL_3)
