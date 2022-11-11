"""Conftest for conversion logic."""
from typing import Any, Callable, Dict, List, Optional, Union, cast

import py
import pytest
from pydantic import parse_obj_as

from emulation_system import OpentronsEmulationConfiguration, SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    MountTypes,
    OpentronsRepository,
    SourceType,
)
from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.images import (
    HeaterShakerModuleImages,
    MagneticModuleImages,
    RobotServerImages,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)
from emulation_system.compose_file_creator.output.compose_file_model import Volume1
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)

CONTAINER_NAME_TO_IMAGE = {
    OT2_ID: RobotServerImages().local_firmware_image_name,
    THERMOCYCLER_MODULE_ID: ThermocyclerModuleImages().local_hardware_image_name,
    HEATER_SHAKER_MODULE_ID: HeaterShakerModuleImages().remote_hardware_image_name,
    TEMPERATURE_MODULE_ID: TemperatureModuleImages().local_firmware_image_name,
    MAGNETIC_MODULE_ID: MagneticModuleImages().local_firmware_image_name,
}

SERVICE_NAMES = [
    OT2_ID,
    THERMOCYCLER_MODULE_ID,
    HEATER_SHAKER_MODULE_ID,
    TEMPERATURE_MODULE_ID,
    MAGNETIC_MODULE_ID,
]

EXTRA_MOUNT_PATH = "/var/log/log_files"
FAKE_COMMIT_ID = "ca82a6dff817ec66f44342007202690a93763949"


@pytest.fixture
def robot_with_mount_and_modules_services(
    tmpdir: py.path.local,
    ot2_only: Dict[str, Any],
    modules_only: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
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
        convert_from_obj(ot2_only, testing_global_em_config, False).services,
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
def opentrons_head(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return head url of opentrons repo from test config file."""
    return testing_global_em_config.get_repo_head(OpentronsRepository.OPENTRONS)


@pytest.fixture
def ot3_firmware_head(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return head url of ot3-firmware repo from test config file."""
    return testing_global_em_config.get_repo_head(OpentronsRepository.OT3_FIRMWARE)


@pytest.fixture
def opentrons_commit(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return commit url of opentrons repo from test config file."""
    return testing_global_em_config.get_repo_commit(
        OpentronsRepository.OPENTRONS
    ).replace("{{commit-sha}}", FAKE_COMMIT_ID)


@pytest.fixture
def ot3_firmware_commit(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> str:
    """Return commit url of ot3-firmware repo from test config file."""
    return testing_global_em_config.get_repo_commit(
        OpentronsRepository.OT3_FIRMWARE
    ).replace("{{commit-sha}}", FAKE_COMMIT_ID)


@pytest.fixture
def robot_set_source_type_params(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    """Create a runnable fixture that builds a RuntimeComposeFileModel."""

    def robot_set_source_type_params(
        robot_dict: Dict[str, Any],
        source_type: SourceType,
        source_location: str,
        robot_server_source_type: SourceType,
        robot_server_source_location: str,
        can_server_source_type: Optional[SourceType],
        can_server_source_location: Optional[str],
        opentrons_hardware_source_type: Optional[SourceType],
        opentrons_hardware_source_location: Optional[str],
    ) -> Dict[str, Any]:
        robot_dict["source-type"] = source_type
        robot_dict["source-location"] = source_location
        robot_dict["robot-server-source-type"] = robot_server_source_type
        robot_dict["robot-server-source-location"] = robot_server_source_location

        if (
            can_server_source_type is not None
            and can_server_source_location is not None
        ):
            robot_dict["can-server-source-type"] = can_server_source_type
            robot_dict["can-server-source-location"] = can_server_source_location

        if (
            opentrons_hardware_source_type is not None
            and opentrons_hardware_source_location is not None
        ):
            robot_dict[
                "opentrons-hardware-source-type"
            ] = opentrons_hardware_source_type
            robot_dict[
                "opentrons-hardware-source-location"
            ] = opentrons_hardware_source_location
        return {"robot": robot_dict}

    return robot_set_source_type_params


@pytest.fixture
def module_set_source_type_params(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> Callable:
    """Create a runnable fixture that builds a RuntimeComposeFileModel."""

    def module_set_source_type_params(
        module_dict: Dict[str, Any],
        source_type: SourceType,
        source_location: str,
        emulation_level: EmulationLevels,
    ) -> SystemConfigurationModel:
        module_dict["source-type"] = source_type
        module_dict["source-location"] = source_location
        module_dict["emulation-level"] = emulation_level
        return parse_obj_as(SystemConfigurationModel, {"modules": [module_dict]})

    return module_set_source_type_params


@pytest.fixture
def ot3_remote_everything_latest(
    ot3_default: Dict[str, Any], robot_set_source_type_params: Callable
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location="latest",
        opentrons_hardware_source_type=SourceType.REMOTE,
        opentrons_hardware_source_location="latest",
    )


@pytest.fixture
def ot3_remote_everything_commit_id(
    ot3_default: Dict[str, Any], robot_set_source_type_params: Callable
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location=FAKE_COMMIT_ID,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location=FAKE_COMMIT_ID,
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location=FAKE_COMMIT_ID,
        opentrons_hardware_source_type=SourceType.REMOTE,
        opentrons_hardware_source_location=FAKE_COMMIT_ID,
    )


@pytest.fixture
def ot3_local_source(
    ot3_default: Dict[str, Any],
    ot3_firmware_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.LOCAL,
        source_location=ot3_firmware_dir,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location="latest",
        opentrons_hardware_source_type=SourceType.REMOTE,
        opentrons_hardware_source_location="latest",
    )


@pytest.fixture
def ot3_remote_source_local_opentrons_hardware(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location="latest",
        opentrons_hardware_source_type=SourceType.LOCAL,
        opentrons_hardware_source_location=opentrons_dir,
    )


@pytest.fixture
def ot3_local_can(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.LOCAL,
        can_server_source_location=opentrons_dir,
        opentrons_hardware_source_type=SourceType.REMOTE,
        opentrons_hardware_source_location="latest",
    )


@pytest.fixture
def ot3_local_robot(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location="latest",
        opentrons_hardware_source_type=SourceType.REMOTE,
        opentrons_hardware_source_location="latest",
    )


@pytest.fixture
def ot3_local_everything(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    ot3_firmware_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.LOCAL,
        source_location=ot3_firmware_dir,
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=SourceType.LOCAL,
        can_server_source_location=opentrons_dir,
        opentrons_hardware_source_type=SourceType.LOCAL,
        opentrons_hardware_source_location=opentrons_dir,
    )


@pytest.fixture
def ot3_local_opentrons_hardware(
    ot3_default: Dict[str, Any],
    opentrons_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot3_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=SourceType.REMOTE,
        can_server_source_location="latest",
        opentrons_hardware_source_type=SourceType.LOCAL,
        opentrons_hardware_source_location=opentrons_dir,
    )


@pytest.fixture
def ot2_remote_everything_latest(
    ot2_default: Dict[str, Any], robot_set_source_type_params: Callable
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=None,
        can_server_source_location=None,
        opentrons_hardware_source_type=None,
        opentrons_hardware_source_location=None,
    )


@pytest.fixture
def ot2_remote_everything_commit_id(
    ot2_default: Dict[str, Any], robot_set_source_type_params: Callable
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.REMOTE,
        source_location=FAKE_COMMIT_ID,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location=FAKE_COMMIT_ID,
        can_server_source_type=None,
        can_server_source_location=None,
        opentrons_hardware_source_type=None,
        opentrons_hardware_source_location=None,
    )


@pytest.fixture
def ot2_local_source(
    ot2_default: Dict[str, Any],
    opentrons_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.LOCAL,
        source_location=opentrons_dir,
        robot_server_source_type=SourceType.REMOTE,
        robot_server_source_location="latest",
        can_server_source_type=None,
        can_server_source_location=None,
        opentrons_hardware_source_type=None,
        opentrons_hardware_source_location=None,
    )


@pytest.fixture
def ot2_local_robot(
    ot2_default: Dict[str, Any],
    opentrons_dir: str,
    robot_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return robot_set_source_type_params(
        robot_dict=ot2_default,
        source_type=SourceType.REMOTE,
        source_location="latest",
        robot_server_source_type=SourceType.LOCAL,
        robot_server_source_location=opentrons_dir,
        can_server_source_type=None,
        can_server_source_location=None,
        opentrons_hardware_source_type=None,
        opentrons_hardware_source_location=None,
    )


@pytest.fixture
def heater_shaker_module_hardware_local(
    heater_shaker_module_default: Dict[str, Any],
    opentrons_modules_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return module_set_source_type_params(
        module_dict=heater_shaker_module_default,
        source_type="local",
        source_location=opentrons_modules_dir,
        emulation_level="hardware",
    )


@pytest.fixture
def heater_shaker_module_hardware_remote(
    heater_shaker_module_default: Dict[str, Any],
    opentrons_modules_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return module_set_source_type_params(
        module_dict=heater_shaker_module_default,
        source_type="remote",
        source_location="latest",
        emulation_level="hardware",
    )


@pytest.fixture
def thermocycler_module_firmware_local(
    thermocycler_module_default: Dict[str, Any],
    opentrons_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return module_set_source_type_params(
        module_dict=thermocycler_module_default,
        source_type="local",
        source_location=opentrons_dir,
        emulation_level="firmware",
    )


@pytest.fixture
def thermocycler_module_hardware_local(
    thermocycler_module_default: Dict[str, Any],
    opentrons_modules_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return module_set_source_type_params(
        module_dict=thermocycler_module_default,
        source_type="local",
        source_location=opentrons_modules_dir,
        emulation_level="hardware",
    )


@pytest.fixture
def thermocycler_module_firmware_remote(
    thermocycler_module_default: Dict[str, Any],
    opentrons_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return module_set_source_type_params(
        module_dict=thermocycler_module_default,
        source_type="remote",
        source_location="latest",
        emulation_level="firmware",
    )


@pytest.fixture
def thermocycler_module_hardware_remote(
    thermocycler_module_default: Dict[str, Any],
    opentrons_modules_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return module_set_source_type_params(
        module_dict=thermocycler_module_default,
        source_type="remote",
        source_location="latest",
        emulation_level="hardware",
    )


@pytest.fixture
def temperature_module_firmware_local(
    temperature_module_default: Dict[str, Any],
    opentrons_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return module_set_source_type_params(
        module_dict=temperature_module_default,
        source_type="local",
        source_location=opentrons_dir,
        emulation_level="firmware",
    )


@pytest.fixture
def temperature_module_firmware_remote(
    temperature_module_default: Dict[str, Any],
    opentrons_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return module_set_source_type_params(
        module_dict=temperature_module_default,
        source_type="remote",
        source_location="latest",
        emulation_level="firmware",
    )


@pytest.fixture
def magnetic_module_firmware_remote(
    magnetic_module_default: Dict[str, Any],
    opentrons_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return module_set_source_type_params(
        module_dict=magnetic_module_default,
        source_type="remote",
        source_location="latest",
        emulation_level="firmware",
    )


@pytest.fixture
def magnetic_module_firmware_local(
    magnetic_module_default: Dict[str, Any],
    opentrons_dir: str,
    module_set_source_type_params: Callable,
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return module_set_source_type_params(
        module_dict=magnetic_module_default,
        source_type="local",
        source_location=opentrons_dir,
        emulation_level="firmware",
    )
