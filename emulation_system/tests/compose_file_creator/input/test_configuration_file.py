"""Tests for SystemConfigurationModel class.

Note: Do not need to test matching module names because module names cannot be the same
by definition of dict.
"""
from typing import Any, Callable, Dict

import pytest
from pydantic import ValidationError
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import SystemConfigurationModel
from emulation_system.compose_file_creator.errors import DuplicateHardwareNameError
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    OT2InputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    SYSTEM_UNIQUE_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)


@pytest.fixture
def matching_module_names(make_config: Callable) -> Dict[str, Any]:
    """Dict with matching moudle names."""
    config = make_config(modules={"magnetic-module": 1})
    config["modules"].extend(config["modules"])
    return config


@pytest.fixture
def matching_robot_and_module_names(make_config: Callable) -> Dict[str, Any]:
    """Dict with matching robot and module name."""
    config = make_config(robot="ot2", modules={"magnetic-module": 1})
    config["robot"]["id"] = config["modules"][0]["id"]
    return config


@pytest.fixture
def invalid_ot2_name(make_config: Callable) -> Dict[str, Any]:
    """Dict with ot2 that has invalid name."""
    config = make_config(robot="ot2")
    config["robot"]["id"] = "Invalid Name"
    return config


@pytest.fixture
def null_robot_with_modules(make_config: Callable) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules and null robot."""
    config = make_config(
        robot="ot2",
        modules={
            "magnetic-module": 1,
            "temperature-module": 1,
            "thermocycler-module": 1,
            "heater-shaker-module": 1,
        },
        system_unique_id="test",
    )
    config["robot"] = None
    config["system-unique-id"] = None
    return config


@pytest.fixture
def null_module_with_robot(make_config: Callable) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules and null robot."""
    config = make_config(
        robot="ot2",
        modules={
            "magnetic-module": 1,
            "temperature-module": 1,
            "thermocycler-module": 1,
            "heater-shaker-module": 1,
        },
        system_unique_id="test",
    )
    config["modules"] = None
    config["system-unique-id"] = None
    return config


@pytest.fixture
def null_everything() -> Dict[str, None]:
    """Structure of SystemConfigurationModel with all values null."""
    return {
        "robot": None,
        "modules": None,
        "system-unique-id": None,
    }


@pytest.fixture
def with_invalid_system_unique_id(make_config: Callable) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and an invalid system-unique-id."""
    config = make_config(
        robot="ot2",
        modules={
            "magnetic-module": 1,
            "temperature-module": 1,
            "thermocycler-module": 1,
            "heater-shaker-module": 1,
        },
        system_unique_id="test",
    )
    config["system-unique-id"] = "I aM uNiQuE bUt InVaLiD"
    return config


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("matching_robot_and_module_names"),
        lazy_fixture("matching_module_names"),
    ],
)
def test_duplicate_names(config: Dict[str, Any]) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""
    with pytest.raises(DuplicateHardwareNameError) as err:
        SystemConfigurationModel.from_dict(config)
    expected_error_text = (
        "The following container names are duplicated in the "
        f"configuration file: {MAGNETIC_MODULE_ID}"
    )
    assert err.match(expected_error_text)


def test_invalid_container_name(invalid_ot2_name: Dict[str, Any]) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""
    with pytest.raises(ValidationError) as err:
        SystemConfigurationModel.from_dict(invalid_ot2_name)
    expected_error_text = ".*string does not match regex.*"
    assert err.match(expected_error_text)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("modules_only"),
        lazy_fixture("ot2_and_modules"),
        lazy_fixture("null_robot_with_modules"),
    ],
)
def test_modules_exist_is_true(config: Dict[str, Any]) -> None:
    """Test that modules_exist property is true when it is supposed to be."""
    assert SystemConfigurationModel.from_dict(config).modules_exist


@pytest.mark.parametrize(
    "config", [lazy_fixture("ot2_only"), lazy_fixture("null_module_with_robot")]
)
def test_modules_exist_is_false(config: Dict[str, Any]) -> None:
    """Test that modules_exist property is false when it is supposed to be."""
    assert not SystemConfigurationModel.from_dict(config).modules_exist


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("ot2_only"),
        lazy_fixture("ot2_and_modules"),
        lazy_fixture("null_module_with_robot"),
    ],
)
def test_robot_exists_is_true(config: Dict[str, Any]) -> None:
    """Test that robot_exists property is true when it is supposed to be."""
    assert SystemConfigurationModel.from_dict(config).robot_exists


@pytest.mark.parametrize(
    "config", [lazy_fixture("modules_only"), lazy_fixture("null_robot_with_modules")]
)
def test_robot_exists_is_false(config: Dict[str, Any]) -> None:
    """Test that robot_exists property is false when it is supposed to be."""
    assert not SystemConfigurationModel.from_dict(config).robot_exists


def test_containers_property(ot2_and_modules: Dict[str, Any]) -> None:
    """Test the containers property is constructed correctly."""
    containers = SystemConfigurationModel.from_dict(ot2_and_modules).containers
    magnetic_module_id = f"{MAGNETIC_MODULE_ID}-1"
    temperature_module_id = f"{TEMPERATURE_MODULE_ID}-1"
    thermocycler_module_id = f"{THERMOCYCLER_MODULE_ID}-1"
    heater_shaker_module_id = f"{HEATER_SHAKER_MODULE_ID}-1"

    assert set(containers.keys()) == {
        OT2_ID,
        magnetic_module_id,
        temperature_module_id,
        thermocycler_module_id,
        heater_shaker_module_id,
    }
    assert isinstance(containers[OT2_ID], OT2InputModel)
    assert isinstance(containers[magnetic_module_id], MagneticModuleInputModel)
    assert isinstance(containers[temperature_module_id], TemperatureModuleInputModel)
    assert isinstance(containers[thermocycler_module_id], ThermocyclerModuleInputModel)
    assert isinstance(containers[heater_shaker_module_id], HeaterShakerModuleInputModel)


def test_get_by_id(ot2_and_modules: Dict[str, Any]) -> None:
    """Test that loading containers by id works correctly."""
    system_config = SystemConfigurationModel.from_dict(ot2_and_modules)
    magnetic_module_id = f"{MAGNETIC_MODULE_ID}-1"
    temperature_module_id = f"{TEMPERATURE_MODULE_ID}-1"
    thermocycler_module_id = f"{THERMOCYCLER_MODULE_ID}-1"
    heater_shaker_module_id = f"{HEATER_SHAKER_MODULE_ID}-1"
    assert isinstance(system_config.get_by_id(OT2_ID), OT2InputModel)
    assert isinstance(
        system_config.get_by_id(heater_shaker_module_id), HeaterShakerModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id(magnetic_module_id), MagneticModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id(temperature_module_id), TemperatureModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id(thermocycler_module_id), ThermocyclerModuleInputModel
    )


@pytest.mark.parametrize(
    "config", [lazy_fixture("ot2_and_modules"), lazy_fixture("null_everything")]
)
def test_no_system_unique_id(config: Dict[str, Any]) -> None:
    """Test that default network name is set correctly when field is not specified."""
    assert SystemConfigurationModel.from_dict(config).system_unique_id is None


def test_overriding_system_unique_id(with_system_unique_id: Dict[str, Any]) -> None:
    """Test that system network name is overridden correctly."""
    system_config = SystemConfigurationModel.from_dict(with_system_unique_id)
    assert system_config.system_unique_id == SYSTEM_UNIQUE_ID


def test_invalid_system_unique_id(
    with_invalid_system_unique_id: Dict[str, Any]
) -> None:
    """Verify exception is thrown when invalid system-unique-id is passed."""
    with pytest.raises(ValidationError):
        SystemConfigurationModel.from_dict(with_invalid_system_unique_id)
