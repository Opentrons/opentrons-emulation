"""Tests for SystemConfigurationModel class.

Note: Do not need to test matching module names because module names cannot be the same
by definition of dict.
"""
import pathlib
from typing import Any, Dict

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
def matching_module_names(magnetic_module_default: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with matching moudle names."""
    return {"modules": [magnetic_module_default, magnetic_module_default]}


@pytest.fixture
def matching_robot_and_module_names(
    magnetic_module_default: Dict[str, Any], ot2_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Dict with matching robot and module name."""
    ot2_default["id"] = MAGNETIC_MODULE_ID
    return {"robot": ot2_default, "modules": [magnetic_module_default]}


@pytest.fixture
def invalid_ot2_name(ot2_default: Dict[str, Any]) -> Dict[str, Any]:
    """Dict with ot2 that has invalid name."""
    ot2_default["id"] = "Invalid Name"
    return {"robot": ot2_default}


@pytest.fixture
def null_robot_with_modules(modules_only: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules and null robot."""
    modules_only["robot"] = None
    modules_only["system-unique-id"] = None
    return modules_only


@pytest.fixture
def null_module_with_robot(ot2_only: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules and null robot."""
    ot2_only["modules"] = None
    ot2_only["system-unique-id"] = None
    return ot2_only


@pytest.fixture
def null_everything() -> Dict[str, None]:
    """Structure of SystemConfigurationModel with all values null."""
    return {
        "robot": None,
        "modules": None,
        "system-unique-id": None,
    }


@pytest.fixture
def with_invalid_system_unique_id(ot2_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and an invalid system-unique-id."""
    ot2_and_modules["system-unique-id"] = "I aM uNiQuE bUt InVaLiD"
    return ot2_and_modules


@pytest.fixture
def ot2_with_mounts(tmp_path: pathlib.Path, ot2_default: Dict) -> Dict:
    """Configuration of a robot with extra bind mounts."""
    datadog_dir = tmp_path / "Datadog"
    datadog_dir.mkdir()
    datadog_file = datadog_dir / "log.txt"
    datadog_file.write_text("test")

    log_dir = tmp_path / "Log"
    log_dir.mkdir()

    ot2_default["robot"][OT2_ID]["extra-mounts"] = [
        {
            "name": "DATADOG",
            "source-path": str(datadog_file),
            "mount-path": "/datadog/log.txt",
            "type": "file",
        },
        {
            "name": "LOG_FILES",
            "source-path": str(log_dir),
            "mount-path": "/var/log/opentrons/",
            "type": "directory",
        },
    ]
    return ot2_default


def create_system_configuration(obj: Dict) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel object."""
    return SystemConfigurationModel.from_dict(obj)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("matching_robot_and_module_names"),
        lazy_fixture("matching_module_names"),
    ],
)
def test_duplicate_names(config: Dict[str, Any]) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""
    print(config)
    with pytest.raises(DuplicateHardwareNameError) as err:
        create_system_configuration(config)
    expected_error_text = (
        "The following container names are duplicated in the "
        f"configuration file: {MAGNETIC_MODULE_ID}"
    )
    assert err.match(expected_error_text)


def test_invalid_container_name(invalid_ot2_name: Dict[str, Any]) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""
    with pytest.raises(ValidationError) as err:
        create_system_configuration(invalid_ot2_name)
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
    assert create_system_configuration(config).modules_exist


@pytest.mark.parametrize(
    "config", [lazy_fixture("ot2_only"), lazy_fixture("null_module_with_robot")]
)
def test_modules_exist_is_false(config: Dict[str, Any]) -> None:
    """Test that modules_exist property is false when it is supposed to be."""
    assert not create_system_configuration(config).modules_exist


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
    assert create_system_configuration(config).robot_exists


@pytest.mark.parametrize(
    "config", [lazy_fixture("modules_only"), lazy_fixture("null_robot_with_modules")]
)
def test_robot_exists_is_false(config: Dict[str, Any]) -> None:
    """Test that robot_exists property is false when it is supposed to be."""
    assert not create_system_configuration(config).robot_exists


def test_containers_property(ot2_and_modules: Dict[str, Any]) -> None:
    """Test the containers property is constructed correctly."""
    containers = create_system_configuration(ot2_and_modules).containers
    assert set(containers.keys()) == {
        OT2_ID,
        MAGNETIC_MODULE_ID,
        TEMPERATURE_MODULE_ID,
        THERMOCYCLER_MODULE_ID,
        HEATER_SHAKER_MODULE_ID,
    }
    assert isinstance(containers[OT2_ID], OT2InputModel)
    assert isinstance(containers[MAGNETIC_MODULE_ID], MagneticModuleInputModel)
    assert isinstance(containers[TEMPERATURE_MODULE_ID], TemperatureModuleInputModel)
    assert isinstance(containers[THERMOCYCLER_MODULE_ID], ThermocyclerModuleInputModel)
    assert isinstance(containers[HEATER_SHAKER_MODULE_ID], HeaterShakerModuleInputModel)


def test_get_by_id(ot2_and_modules: Dict[str, Any]) -> None:
    """Test that loading containers by id works correctly."""
    system_config = create_system_configuration(ot2_and_modules)
    assert isinstance(system_config.get_by_id(OT2_ID), OT2InputModel)
    assert isinstance(
        system_config.get_by_id(HEATER_SHAKER_MODULE_ID), HeaterShakerModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id(MAGNETIC_MODULE_ID), MagneticModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id(TEMPERATURE_MODULE_ID), TemperatureModuleInputModel
    )
    assert isinstance(
        system_config.get_by_id(THERMOCYCLER_MODULE_ID), ThermocyclerModuleInputModel
    )


@pytest.mark.parametrize(
    "config", [lazy_fixture("ot2_and_modules"), lazy_fixture("null_everything")]
)
def test_no_system_unique_id(config: Dict[str, Any]) -> None:
    """Test that default network name is set correctly when field is not specified."""
    assert create_system_configuration(config).system_unique_id is None


def test_overriding_system_unique_id(with_system_unique_id: Dict[str, Any]) -> None:
    """Test that system network name is overridden correctly."""
    system_config = create_system_configuration(with_system_unique_id)
    assert system_config.system_unique_id == SYSTEM_UNIQUE_ID


def test_invalid_system_unique_id(
    with_invalid_system_unique_id: Dict[str, Any]
) -> None:
    """Verify exception is thrown when invalid system-unique-id is passed."""
    with pytest.raises(ValidationError):
        create_system_configuration(with_invalid_system_unique_id)
