"""Tests for SystemConfigurationModel class.

Note: Do not need to test matching module names because module names cannot be the same
by definition of dict.
"""
from typing import (
    Any,
    Dict,
)

import pytest
from pydantic import ValidationError
from pytest_lazyfixture import lazy_fixture

from emulation_system.compose_file_creator.input.configuration_file import (
    DuplicateHardwareNameError,
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    OT2InputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DEFAULT_DOCKER_COMPOSE_VERSION,
)
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
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
def ot2_with_invalid_mounts(ot2_with_mounts: Dict) -> Dict:
    """Configuration with an invalid mount name."""
    ot2_with_mounts["robot"][OT2_ID]["extra-mounts"][0]["name"] = "data-dog"
    return ot2_with_mounts


@pytest.fixture
def robot_only(ot2_default: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot only."""
    return {"robot": ot2_default}


@pytest.fixture
def modules_only(
    thermocycler_module_default: Dict[str, Any],
    temperature_module_default: Dict[str, Any],
    magnetic_module_default: Dict[str, Any],
    heater_shaker_module_default: Dict[str, Any],
) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules only."""
    return {
        "modules": [
            thermocycler_module_default,
            temperature_module_default,
            magnetic_module_default,
            heater_shaker_module_default,
        ]
    }


@pytest.fixture
def robot_and_modules(
    modules_only: Dict[str, Any], ot2_default: Dict[str, Any]
) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot and modules."""
    modules_only["robot"] = ot2_default
    return modules_only


@pytest.fixture
def version_defined(robot_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and version."""
    robot_and_modules["compose-file-version"] = "3.7"
    return robot_and_modules


@pytest.fixture
def null_robot_with_modules(modules_only: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules and null robot."""
    modules_only["robot"] = None
    modules_only["compose-file-version"] = None
    modules_only["system-unique-id"] = None
    return modules_only


@pytest.fixture
def null_module_with_robot(robot_only: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with modules and null robot."""
    robot_only["modules"] = None
    robot_only["compose-file-version"] = None
    robot_only["system-unique-id"] = None
    return robot_only


@pytest.fixture
def null_everything() -> Dict[str, None]:
    """Structure of SystemConfigurationModel with all values null."""
    return {
        "compose-file-version": None,
        "robot": None,
        "modules": None,
        "system-unique-id": None,
    }


@pytest.fixture
def with_system_unique_id(robot_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and system-unique-id."""  # noqa: E501
    robot_and_modules["system-unique-id"] = "you-have-passed-the-test"
    return robot_and_modules


@pytest.fixture
def with_invalid_system_unique_id(robot_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and an invalid system-unique-id."""  # noqa: E501
    robot_and_modules["system-unique-id"] = "I aM uNiQuE bUt InVaLiD"
    return robot_and_modules


def create_system_configuration(obj: Dict) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel object."""
    return SystemConfigurationModel.from_dict(obj)


def create_system_configuration_from_file(path: str) -> SystemConfigurationModel:
    """Creates SystemConfigurationModel object from config file."""
    return SystemConfigurationModel.from_file(path)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("matching_robot_and_module_names"),
        lazy_fixture("matching_module_names"),
    ],
)
def test_duplicate_names(config: Dict[str, Any]) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""  # noqa: E501
    print(config)
    with pytest.raises(DuplicateHardwareNameError) as err:
        create_system_configuration(config)
    expected_error_text = (
        "The following container names are duplicated in the "
        f"configuration file: {MAGNETIC_MODULE_ID}"
    )
    assert err.match(expected_error_text)


def test_invalid_container_name(invalid_ot2_name: Dict[str, Any]) -> None:
    """Confirm that ValidationError is thrown when a robot and module have the same name."""  # noqa: E501
    with pytest.raises(ValidationError) as err:
        create_system_configuration(invalid_ot2_name)
    expected_error_text = ".*string does not match regex.*"
    assert err.match(expected_error_text)


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("modules_only"),
        lazy_fixture("robot_and_modules"),
        lazy_fixture("null_robot_with_modules"),
    ],
)
def test_modules_exist_is_true(config: Dict[str, Any]) -> None:
    """Test that modules_exist property is true when it is supposed to be."""
    assert create_system_configuration(config).modules_exist


@pytest.mark.parametrize(
    "config", [lazy_fixture("robot_only"), lazy_fixture("null_module_with_robot")]
)
def test_modules_exist_is_false(config: Dict[str, Any]) -> None:
    """Test that modules_exist property is false when it is supposed to be."""
    assert not create_system_configuration(config).modules_exist


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture("robot_only"),
        lazy_fixture("robot_and_modules"),
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


def test_containers_property(robot_and_modules: Dict[str, Any]) -> None:
    """Test the containers property is constructed correctly."""
    containers = create_system_configuration(robot_and_modules).containers
    assert set(containers.keys()) == {
        OT2_ID,
        MAGNETIC_MODULE_ID,
        TEMPERATURE_MODULE_ID,
        THERMOCYCLER_MODULE_ID,
        HEATER_SHAKER_MODULE_ID
    }
    assert isinstance(containers[OT2_ID], OT2InputModel)
    assert isinstance(containers[MAGNETIC_MODULE_ID], MagneticModuleInputModel)
    assert isinstance(containers[TEMPERATURE_MODULE_ID], TemperatureModuleInputModel)
    assert isinstance(containers[THERMOCYCLER_MODULE_ID], ThermocyclerModuleInputModel)
    assert isinstance(containers[HEATER_SHAKER_MODULE_ID], HeaterShakerModuleInputModel)


def test_get_by_id(robot_and_modules: Dict[str, Any]) -> None:
    """Test that loading containers by id works correctly."""
    system_config = create_system_configuration(robot_and_modules)
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
    "config", [lazy_fixture("robot_and_modules"), lazy_fixture("null_everything")]
)
def test_default_version(config: Dict[str, Any]) -> None:
    """Test that version is set to default when not specified."""
    system_config = create_system_configuration(config)
    assert system_config.compose_file_version == DEFAULT_DOCKER_COMPOSE_VERSION


def test_overriding_version(version_defined: Dict[str, Any]) -> None:
    """Test that version is overridden correctly."""
    system_config = create_system_configuration(version_defined)
    assert system_config.compose_file_version == "3.7"


@pytest.mark.parametrize(
    "config", [lazy_fixture("robot_and_modules"), lazy_fixture("null_everything")]
)
def test_no_system_unique_id(config: Dict[str, Any]) -> None:
    """Test that default network name is set correctly when field is not specified."""
    assert create_system_configuration(config).system_unique_id is None


def test_overriding_system_unique_id(with_system_unique_id: Dict[str, Any]) -> None:
    """Test that system network name is overridden correctly."""
    system_config = create_system_configuration(with_system_unique_id)
    assert system_config.system_unique_id == "you-have-passed-the-test"


def test_invalid_system_unique_id(
    with_invalid_system_unique_id: Dict[str, Any]
) -> None:
    """Verify exception is thrown when invalid system-unique-id is passed."""
    with pytest.raises(ValidationError):
        create_system_configuration(test_invalid_system_unique_id)
