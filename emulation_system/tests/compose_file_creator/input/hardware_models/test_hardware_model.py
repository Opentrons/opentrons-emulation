"""Tests for confirming returned image names are correct."""
import pathlib
from typing import Callable, Dict, Optional

import pytest
from pydantic import ValidationError, parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import SystemConfigurationModel
from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    Mount,
)
from emulation_system.compose_file_creator.errors import ImageNotDefinedError
from emulation_system.compose_file_creator.images import get_image_name
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
)

CONFIGURATIONS = [
    # OT2
    [
        Hardware.OT2,
        EmulationLevels.HARDWARE,
        "robot-server",
    ],
    [
        Hardware.OT2,
        EmulationLevels.HARDWARE,
        "robot-server",
    ],
    [
        Hardware.OT2,
        EmulationLevels.FIRMWARE,
        "robot-server",
    ],
    [
        Hardware.OT2,
        EmulationLevels.FIRMWARE,
        "robot-server",
    ],
    # Heater Shaker Module
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.HARDWARE,
        "heater-shaker-hardware",
    ],
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.HARDWARE,
        "heater-shaker-hardware",
    ],
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.FIRMWARE,
        "heater-shaker-firmware",
    ],
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.FIRMWARE,
        "heater-shaker-firmware",
    ],
    # Temperature Module
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.HARDWARE,
        None,
    ],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.HARDWARE,
        None,
    ],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.FIRMWARE,
        "tempdeck-firmware",
    ],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.FIRMWARE,
        "tempdeck-firmware",
    ],
    # Thermocycler Module
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.HARDWARE,
        "thermocycler-hardware",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.HARDWARE,
        "thermocycler-hardware",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.FIRMWARE,
        "thermocycler-firmware",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.FIRMWARE,
        "thermocycler-firmware",
    ],
    # Magnetic Module
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.HARDWARE,
        None,
    ],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.HARDWARE,
        None,
    ],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.FIRMWARE,
        "magdeck-firmware",
    ],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.FIRMWARE,
        "magdeck-firmware",
    ],
]


@pytest.fixture
def file_mount(tmp_path: pathlib.Path) -> Dict[str, str]:
    """Returns FileMount object."""
    datadog_dir = tmp_path / "Datadog"
    datadog_dir.mkdir()
    datadog_file = datadog_dir / "log.txt"
    datadog_file.write_text("test")

    return {
        "source-path": str(datadog_file),
        "mount-path": "/datadog/log.txt",
        "type": "file",
    }


@pytest.fixture
def directory_mount(tmp_path: pathlib.Path) -> Dict[str, str]:
    """Returns DirectoryMount object."""
    log_dir = tmp_path / "Log"
    log_dir.mkdir()
    return {
        "source-path": str(log_dir),
        "mount-path": "/var/log/opentrons/",
        "type": "directory",
    }


@pytest.fixture
def source_mount(tmp_path: pathlib.Path) -> str:
    """Returns mount to source repo."""
    log_dir = tmp_path / "opentrons-modules/"
    log_dir.mkdir()

    return str(log_dir)


@pytest.fixture
def bad_mount_name(directory_mount: Dict[str, str]) -> Dict[str, str]:
    """Create a Directory mount with an invalid name."""
    directory_mount["name"] = "A bad mount name"
    return directory_mount


@pytest.mark.parametrize(
    "hardware,emulation_level,expected_image",
    CONFIGURATIONS,
)
def test_getting_image(
    hardware: Hardware,
    emulation_level: EmulationLevels,
    expected_image: Optional[str],
) -> None:
    """Confirm that correct image is returned, otherwise config exception is thrown if image is not defined."""
    if expected_image is None:
        with pytest.raises(ImageNotDefinedError):
            get_image_name(hardware, emulation_level)
    else:
        assert get_image_name(hardware, emulation_level) == expected_image


def test_get_image_name_from_hardware_model() -> None:
    """Test that get_image_name_from_hardware_model returns correct value."""
    model = HeaterShakerModuleInputModel.parse_obj(
        {
            "id": "my-heater-shaker",
            "hardware": Hardware.HEATER_SHAKER_MODULE,
            "emulation-level": EmulationLevels.HARDWARE,
        }
    )
    assert model.get_image_name() == "heater-shaker-hardware"


@pytest.mark.parametrize(
    "mount,expected_value",
    [
        [lazy_fixture("file_mount"), "/Datadog/log.txt:/datadog/log.txt"],
        [lazy_fixture("directory_mount"), "/Log:/var/log/opentrons/"],
    ],
)
def test_get_bind_mount_string(mount: Mount, expected_value: str) -> None:
    """Confirm file bind mount string is formatted correctly."""
    assert parse_obj_as(Mount, mount).get_bind_mount_string().endswith(expected_value)


def test_duplicate_mounts(file_mount: Dict[str, str]) -> None:
    """Confirm that duplicate mounts are not allowed."""
    with pytest.raises(ValidationError, match=".*Cannot have duplicate mounts"):
        HeaterShakerModuleInputModel.parse_obj(
            {
                "id": "my-heater-shaker",
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "emulation-level": EmulationLevels.HARDWARE,
                "mounts": [file_mount, file_mount],
            }
        )


def test_exception_thrown_when_local_source_code_does_not_exist() -> None:
    """Confirm LocalSourceDoesNotExistError is thrown when local path does not exist."""
    bad_path = "/this/surely/must/be/a/bad/path"
    with pytest.raises(ValidationError):
        HeaterShakerModuleInputModel.parse_obj(
            {
                "id": "my-heater-shaker",
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "emulation-level": EmulationLevels.HARDWARE,
                "mounts": [
                    {
                        "type": "directory",
                        "mount_path": "/test",
                        "source_path": bad_path,
                    }
                ],
            }
        )


@pytest.mark.parametrize(
    "invalid_location", ["f50cd8bfe2b661ecf928cdb044b33e7d10c294a8"]
)
def test_exception_thrown_when_invalid_remote_source_location(
    invalid_location: str, make_config: Callable
) -> None:
    """Confirm LocalSourceDoesNotExistError is thrown when local path does not exist."""
    config = make_config(robot="ot2")
    config["monorepo-source"] = invalid_location
    with pytest.raises(ValidationError) as err:
        SystemConfigurationModel.from_dict(config)
    assert (
        "Usage of a commit SHA as a reference for a source location is deprecated. Use a branch name instead."
        in str(err.value)
    )


@pytest.mark.parametrize(
    "valid_location",
    [
        "edge",
        "latest",
        "Latest",
        "LATEST",
    ],
)
def test_accepts_valid_remote_source_location(
    valid_location: str, make_config: Callable
) -> None:
    """Confirm LocalSourceDoesNotExistError is thrown when local path does not exist."""
    config = make_config(robot="ot2")
    config["monorepo-source"] = valid_location
    system_config = SystemConfigurationModel.from_dict(config)
    assert system_config.monorepo_source.source_location == valid_location
