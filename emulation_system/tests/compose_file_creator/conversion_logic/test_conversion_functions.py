"""Tests for confirming returned image names are correct."""
import pathlib

import pytest
from pydantic import parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore

from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    DirectoryMount,
    EmulationLevels,
    FileMount,
    Hardware,
    Mount,
    SourceType,
)

CONFIGURATIONS = [
    # OT2
    [Hardware.OT2, EmulationLevels.HARDWARE, SourceType.LOCAL, None],
    [Hardware.OT2, EmulationLevels.HARDWARE, SourceType.REMOTE, None],
    [Hardware.OT2, EmulationLevels.FIRMWARE, SourceType.LOCAL, "robot-server-local"],
    [Hardware.OT2, EmulationLevels.FIRMWARE, SourceType.REMOTE, "robot-server-remote"],
    # Heater Shaker Module
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.LOCAL,
        "heater-shaker-hardware-local",
    ],
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.REMOTE,
        "heater-shaker-hardware-remote",
    ],
    [Hardware.HEATER_SHAKER_MODULE, EmulationLevels.FIRMWARE, SourceType.LOCAL, None],
    [Hardware.HEATER_SHAKER_MODULE, EmulationLevels.FIRMWARE, SourceType.REMOTE, None],
    # Temperature Module
    [Hardware.TEMPERATURE_MODULE, EmulationLevels.HARDWARE, SourceType.LOCAL, None],
    [Hardware.TEMPERATURE_MODULE, EmulationLevels.HARDWARE, SourceType.REMOTE, None],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "tempdeck-firmware-local",
    ],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "tempdeck-firmware-remote",
    ],
    # Thermocycler Module
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.LOCAL,
        "thermocycler-hardware-local",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.REMOTE,
        "thermocycler-hardware-remote",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "thermocycler-firmware-local",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "thermocycler-firmware-remote",
    ],
    # Magnetic Module
    [Hardware.MAGNETIC_MODULE, EmulationLevels.HARDWARE, SourceType.LOCAL, None],
    [Hardware.MAGNETIC_MODULE, EmulationLevels.HARDWARE, SourceType.REMOTE, None],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "magdeck-firmware-local",
    ],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "magdeck-firmware-remote",
    ],
]


@pytest.fixture
def file_mount(tmp_path: pathlib.Path) -> FileMount:
    """Returns FileMount object."""
    datadog_dir = tmp_path / "Datadog"
    datadog_dir.mkdir()
    datadog_file = datadog_dir / "log.txt"
    datadog_file.write_text("test")

    obj = {
        "name": "DATADOG",
        "source-path": str(datadog_file),
        "mount-path": "/datadog/log.txt",
        "type": "file",
    }
    return parse_obj_as(FileMount, obj)


@pytest.fixture
def directory_mount(tmp_path: pathlib.Path) -> DirectoryMount:
    """Returns DirectoryMount object."""
    log_dir = tmp_path / "Log"
    log_dir.mkdir()
    obj = {
        "name": "LOG_FILES",
        "source-path": str(log_dir),
        "mount-path": "/var/log/opentrons/",
        "type": "directory",
    }
    return parse_obj_as(DirectoryMount, obj)


@pytest.fixture
def source_mount(tmp_path: pathlib.Path) -> str:
    """Returns mount to source repo."""
    log_dir = tmp_path / "opentrons-modules/"
    log_dir.mkdir()

    return str(log_dir)


def test_get_image_name_from_hardware_model() -> None:
    """Test that get_image_name_from_hardware_model returns correct value."""
    model = HeaterShakerModuleInputModel(
        id="my-heater-shaker",
        hardware=Hardware.HEATER_SHAKER_MODULE,
        source_type=SourceType.REMOTE,
        source_location="latest",
        emulation_level=EmulationLevels.HARDWARE,
    )
    assert model.get_image_name() == "heater-shaker-hardware-remote"


@pytest.mark.parametrize(
    "mount,expected_value",
    [
        [lazy_fixture("file_mount"), "/Datadog/log.txt:/datadog/log.txt"],
        [lazy_fixture("directory_mount"), "/Log:/var/log/opentrons/"],
    ],
)
def test_get_bind_mount_string(mount: Mount, expected_value: str) -> None:
    """Confirm file bind mount string is formatted correctly."""
    assert mount.get_bind_mount_string().endswith(expected_value)


def test_service_conversion(
    file_mount: FileMount, directory_mount: DirectoryMount, source_mount: str
) -> None:
    """Confirm HardwareModel is converted to Service correctly."""
    model = HeaterShakerModuleInputModel(
        id="my-heater-shaker",
        hardware=Hardware.HEATER_SHAKER_MODULE,
        source_type=SourceType.LOCAL,
        source_location=source_mount,
        emulation_level=EmulationLevels.HARDWARE,
        mounts=[
            {
                "name": "FILE_MOUNT",
                "source-path": file_mount.source_path,
                "mount-path": file_mount.mount_path,
                "type": "file",
            },
            {
                "name": "DIRECTORY_MOUNT",
                "source-path": directory_mount.source_path,
                "mount-path": directory_mount.mount_path,
                "type": "directory",
            },
        ],
    )
    print(model.to_service())
