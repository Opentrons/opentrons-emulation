"""Tests for confirming returned image names are correct."""
import pathlib
from typing import Dict, Optional

import pytest
from pydantic import ValidationError, parse_obj_as
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.config_file_settings import (
    DirectoryMount,
    EmulationLevels,
    FileMount,
    Hardware,
    Mount,
    SourceType,
)
from emulation_system.compose_file_creator.errors import CommitShaNotSupportedError
from emulation_system.compose_file_creator.images import (
    ImageNotDefinedError,
    get_image_name,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
)
from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    LocalSourceDoesNotExistError,
    MountNotFoundError,
    NoMountsDefinedError,
)
from emulation_system.consts import SOURCE_CODE_MOUNT_NAME

CONFIGURATIONS = [
    # OT2
    [
        Hardware.OT2,
        EmulationLevels.HARDWARE,
        SourceType.LOCAL,
        "robot-server-local",
    ],
    [
        Hardware.OT2,
        EmulationLevels.HARDWARE,
        SourceType.REMOTE,
        "robot-server-remote",
    ],
    [
        Hardware.OT2,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "robot-server-local",
    ],
    [
        Hardware.OT2,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "robot-server-remote",
    ],
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
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "heater-shaker-firmware-local",
    ],
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "heater-shaker-firmware-remote",
    ],
    # Temperature Module
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.LOCAL,
        None,
    ],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.REMOTE,
        None,
    ],
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
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.LOCAL,
        None,
    ],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.REMOTE,
        None,
    ],
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
def file_mount(tmp_path: pathlib.Path) -> Dict[str, str]:
    """Returns FileMount object."""
    datadog_dir = tmp_path / "Datadog"
    datadog_dir.mkdir()
    datadog_file = datadog_dir / "log.txt"
    datadog_file.write_text("test")

    return {
        "name": "DATADOG",
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
        "name": "LOG_FILES",
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
def restricted_name_mount(directory_mount: Dict[str, str]) -> Dict[str, str]:
    """Create a Directory mount with a restricted name."""
    directory_mount["name"] = SOURCE_CODE_MOUNT_NAME
    return directory_mount


@pytest.fixture
def bad_mount_name(directory_mount: Dict[str, str]) -> Dict[str, str]:
    """Create a Directory mount with an invalid name."""
    directory_mount["name"] = "A bad mount name"
    return directory_mount


@pytest.mark.parametrize(
    "hardware,emulation_level,source_type,expected_image",
    CONFIGURATIONS,
)
def test_getting_image(
    hardware: Hardware,
    emulation_level: EmulationLevels,
    source_type: SourceType,
    expected_image: Optional[str],
) -> None:
    """Confirm that correct image is returned, otherwise config exception is thrown if image is not defined."""
    if expected_image is None:
        with pytest.raises(ImageNotDefinedError):
            get_image_name(hardware, source_type, emulation_level)
    else:
        assert get_image_name(hardware, source_type, emulation_level) == expected_image


def test_get_image_name_from_hardware_model() -> None:
    """Test that get_image_name_from_hardware_model returns correct value."""
    model = HeaterShakerModuleInputModel.parse_obj(
        {
            "id": "my-heater-shaker",
            "hardware": Hardware.HEATER_SHAKER_MODULE,
            "source-type": SourceType.REMOTE,
            "source-location": "latest",
            "emulation-level": EmulationLevels.HARDWARE,
        }
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
    assert parse_obj_as(Mount, mount).get_bind_mount_string().endswith(expected_value)


def test_restricted_mount(
    restricted_name_mount: DirectoryMount, source_mount: str
) -> None:
    """Confirm exception is thrown when trying to name mount with a restricted name."""
    with pytest.raises(ValidationError) as err:
        HeaterShakerModuleInputModel.parse_obj(
            {
                "id": "my-heater-shaker",
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "source-type": SourceType.LOCAL,
                "source-location": source_mount,
                "emulation-level": EmulationLevels.HARDWARE,
                "mounts": [restricted_name_mount],
            }
        )
    assert err.match("Mount name cannot be any of the following values:.*")


def test_mounts_with_same_names(file_mount: Dict[str, str], source_mount: str) -> None:
    """Confirm exception is thrown when you have mounts with duplicate names."""
    with pytest.raises(ValidationError) as err:
        HeaterShakerModuleInputModel.parse_obj(
            {
                "id": "my-heater-shaker",
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "source-type": SourceType.LOCAL,
                "source-location": source_mount,
                "emulation-level": EmulationLevels.HARDWARE,
                "mounts": [file_mount, file_mount],
            }
        )

    assert err.match('"my-heater-shaker" has mounts with duplicate names')


def test_source_code_mount_created(
    file_mount: Dict[str, str], source_mount: str
) -> None:
    """Confirm SOURCE_CODE mount is created when using local source-type."""
    model = HeaterShakerModuleInputModel.parse_obj(
        {
            "id": "my-heater-shaker",
            "hardware": Hardware.HEATER_SHAKER_MODULE,
            "source-type": SourceType.LOCAL,
            "source-location": source_mount,
            "emulation-level": EmulationLevels.HARDWARE,
            "mounts": [file_mount],
        }
    )

    assert model.get_mount_by_name(SOURCE_CODE_MOUNT_NAME)
    assert model.get_mount_by_name("DATADOG")


def test_source_code_mount_not_created(
    file_mount: Dict[str, str], source_mount: str
) -> None:
    """Confirm SOURCE_CODE mount is not created when using remote source-type."""
    model = HeaterShakerModuleInputModel.parse_obj(
        {
            "id": "my-heater-shaker",
            "hardware": Hardware.HEATER_SHAKER_MODULE,
            "source-type": SourceType.REMOTE,
            "source-location": "latest",
            "emulation-level": EmulationLevels.HARDWARE,
            "mounts": [file_mount],
        }
    )

    assert model.get_mount_by_name("DATADOG")
    with pytest.raises(MountNotFoundError) as err:
        model.get_mount_by_name(SOURCE_CODE_MOUNT_NAME)

    assert err.match(f'Mount named "{SOURCE_CODE_MOUNT_NAME}" not found.')


def test_no_mounts_exist(source_mount: str) -> None:
    """Confirm NoMountsDefinedError is thrown when no mounts exist."""
    model = HeaterShakerModuleInputModel.parse_obj(
        {
            "id": "my-heater-shaker",
            "hardware": Hardware.HEATER_SHAKER_MODULE,
            "source-type": SourceType.REMOTE,
            "source-location": "latest",
            "emulation-level": EmulationLevels.HARDWARE,
            "mounts": [],
        }
    )

    with pytest.raises(NoMountsDefinedError) as err:
        model.get_mount_by_name("Something")

    assert err.match("You have no mounts defined.")


def test_exception_thrown_when_local_source_code_does_not_exist() -> None:
    """Confirm LocalSourceDoesNotExistError is thrown when local path does not exist."""
    bad_path = "/this/surely/must/be/a/bad/path"
    with pytest.raises(LocalSourceDoesNotExistError) as err:
        HeaterShakerModuleInputModel.parse_obj(
            {
                "id": "my-heater-shaker",
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "source-type": SourceType.LOCAL,
                "source-location": bad_path,
                "emulation-level": EmulationLevels.HARDWARE,
                "mounts": [],
            }
        )

    assert err.match(f'"{bad_path}" is not a valid directory path')


@pytest.mark.parametrize(
    "invalid_location", ["f50cd8bfe2b661ecf928cdb044b33e7d10c294a8"]
)
def test_exception_thrown_when_invalid_remote_source_location(
    invalid_location: str,
) -> None:
    """Confirm LocalSourceDoesNotExistError is thrown when local path does not exist."""
    with pytest.raises(CommitShaNotSupportedError):
        HeaterShakerModuleInputModel.parse_obj(
            {
                "id": "my-heater-shaker",
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "source-type": SourceType.REMOTE,
                "source-location": invalid_location,
                "emulation-level": EmulationLevels.HARDWARE,
                "mounts": [],
            }
        )


@pytest.mark.parametrize(
    "valid_location",
    [
        "branch-name",
        "latest",
        "Latest",
        "LATEST",
    ],
)
def test_accepts_valid_remote_source_location(valid_location: str) -> None:
    """Confirm LocalSourceDoesNotExistError is thrown when local path does not exist."""
    hs = HeaterShakerModuleInputModel.parse_obj(
        {
            "id": "my-heater-shaker",
            "hardware": Hardware.HEATER_SHAKER_MODULE,
            "source-type": SourceType.REMOTE,
            "source-location": valid_location,
            "emulation-level": EmulationLevels.HARDWARE,
            "mounts": [],
        }
    )

    assert hs.source_location == valid_location


def test_extra_mounts(file_mount: Dict, directory_mount: Dict) -> None:
    """Test that extra mounts are created correctly."""
    model = HeaterShakerModuleInputModel.parse_obj(
        {
            "id": "my-heater-shaker",
            "hardware": Hardware.HEATER_SHAKER_MODULE,
            "source-type": SourceType.REMOTE,
            "source-location": "latest",
            "emulation-level": EmulationLevels.HARDWARE,
            "mounts": [file_mount, directory_mount],
        }
    )
    datadog_mount = model.get_mount_by_name("DATADOG")
    assert isinstance(datadog_mount, FileMount)
    assert datadog_mount.name == "DATADOG"
    assert datadog_mount.mount_path == "/datadog/log.txt"

    log_mount = model.get_mount_by_name("LOG_FILES")
    assert isinstance(log_mount, DirectoryMount)
    assert log_mount.name == "LOG_FILES"
    assert log_mount.mount_path == "/var/log/opentrons/"


def test_invalid_mount_name(bad_mount_name: Dict) -> None:
    """Test that ValidationError is thrown when you have an invalid mount name."""
    with pytest.raises(ValidationError) as err:
        HeaterShakerModuleInputModel.parse_obj(
            {
                "id": "my-heater-shaker",
                "hardware": Hardware.HEATER_SHAKER_MODULE,
                "source-type": SourceType.REMOTE,
                "source-location": "latest",
                "emulation-level": EmulationLevels.HARDWARE,
                "mounts": [bad_mount_name],
            }
        )
    assert err.match(".*string does not match regex.*")
