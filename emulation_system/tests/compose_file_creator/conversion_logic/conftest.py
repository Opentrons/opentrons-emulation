"""Conftest for conversion logic."""
from typing import Any, Dict, List, Optional, Union, cast

import py
import pytest

from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.config_file_settings import (
    MountTypes,
    OpentronsRepository,
)
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.images import (
    HeaterShakerModuleImages,
    MagneticModuleImages,
    RobotServerImage,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)
from emulation_system.compose_file_creator.output.compose_file_model import Volume1
from tests.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)

CONTAINER_NAME_TO_IMAGE = {
    OT2_ID: RobotServerImage().image_name,
    THERMOCYCLER_MODULE_ID: ThermocyclerModuleImages().hardware_image_name,
    HEATER_SHAKER_MODULE_ID: HeaterShakerModuleImages().hardware_image_name,
    TEMPERATURE_MODULE_ID: TemperatureModuleImages().firmware_image_name,
    MAGNETIC_MODULE_ID: MagneticModuleImages().firmware_image_name,
}

SERVICE_NAMES = [
    OT2_ID,
    THERMOCYCLER_MODULE_ID,
    HEATER_SHAKER_MODULE_ID,
    TEMPERATURE_MODULE_ID,
    MAGNETIC_MODULE_ID,
]

EXTRA_MOUNT_PATH = "/var/log/log_files"
FAKE_BRANCH_NAME = "test-branch-name"


@pytest.fixture
def robot_with_mount_and_modules_services(
    tmpdir: py.path.local,
    ot2_only: Dict[str, Any],
    modules_only: Dict[str, Any],
) -> Dict[str, Service]:
    """Get services from ot2_and_modules."""
    ot2_only["robot"]["extra-mounts"] = [
        {
            "name": "LOG_FILES",
            "type": MountTypes.DIRECTORY,
            "mount-path": EXTRA_MOUNT_PATH,
            "source-path": str(tmpdir.mkdir("log_files")),
        }
    ]
    ot2_only.update(modules_only)
    return cast(
        Dict[str, Service],
        convert_from_obj(ot2_only, False).services,
    )


def partial_string_in_mount(
    string: str, volumes: Optional[List[Union[str, Volume1]]]
) -> bool:
    """Check if the partial string exists in any of the Service's mounts."""
    assert volumes is not None
    return any([string in volume for volume in volumes])


def get_source_code_build_args(service: Service) -> Dict[str, str]:
    """Get build args for service."""
    build = service.build
    assert build is not None
    assert isinstance(build, BuildItem)
    assert build.args is not None
    return cast(Dict[str, str], build.args.__root__)


def build_args_are_none(service: Service) -> bool:
    """Whether or not build args are None. With annoying typing stuff."""
    build = service.build
    assert build is not None
    assert isinstance(build, BuildItem)
    return build.args is None


@pytest.fixture
def opentrons_head() -> str:
    """Return head url of opentrons repo from test config file."""
    return OpentronsRepository.OPENTRONS.default_branch


@pytest.fixture
def ot3_firmware_head() -> str:
    """Return head url of ot3-firmware repo from test config file."""
    return OpentronsRepository.OT3_FIRMWARE.default_branch


@pytest.fixture
def opentrons_branch() -> str:
    """Return branch url of opentrons repo from test config file."""
    return OpentronsRepository.OPENTRONS.get_user_specified_download_url(
        FAKE_BRANCH_NAME
    )


@pytest.fixture
def ot3_firmware_branch() -> str:
    """Return branch url of ot3-firmware repo from test config file."""
    return OpentronsRepository.OT3_FIRMWARE.get_user_specified_download_url(
        FAKE_BRANCH_NAME
    )
