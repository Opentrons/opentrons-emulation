"""Conftest for conversion logic."""
from typing import Any, Callable, Dict, Optional, cast

import py
import pytest

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
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
from tests.compose_file_creator.conftest import (
    FAKE_COMMIT_ID,
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
    f"{THERMOCYCLER_MODULE_ID}-1",
    f"{HEATER_SHAKER_MODULE_ID}-1",
    f"{TEMPERATURE_MODULE_ID}-1",
    f"{MAGNETIC_MODULE_ID}-1",
]

EXTRA_MOUNT_PATH = "/var/log/log_files"


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


def partial_string_in_mount(string: str, service: Service) -> bool:
    """Check if the partial string exists in any of the Service's mounts."""
    volumes = service.volumes
    assert volumes is not None
    return any([string in volume for volume in volumes])


def mount_string_is(string: str, service: Service) -> bool:
    volumes = service.volumes
    assert volumes is not None
    return any([string == volume for volume in volumes])


def check_correct_number_of_volumes(container: Service, expected_number: int) -> None:
    volumes = container.volumes
    if expected_number == 0:
        assert (
            volumes is None
        ), f'Correct number of volumes is 0, you have "{len(volumes)}'
    else:
        assert volumes is not None
        assert (
            len(volumes) == expected_number
        ), f'Correct number of volumes is {expected_number}, you have "{len(volumes)}"'


def get_source_code_build_args(service: Service) -> Optional[Dict[str, str]]:
    """Get build args for service."""
    build = service.build
    assert build is not None
    assert isinstance(build, BuildItem)
    if build.args is None:
        return None
    else:
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
def ot3_remote_everything_commit_id(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(
        robot="ot3", monorepo_source="commit_id", ot3_firmware_source="commit_id"
    )


@pytest.fixture
def ot3_local_ot3_firmware_remote_monorepo(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and remote robot source."""
    return make_config(
        robot="ot3", monorepo_source="latest", ot3_firmware_source="path"
    )


@pytest.fixture
def ot3_remote_ot3_firmware_local_monorepo(
    make_config: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(
        robot="ot3", monorepo_source="path", ot3_firmware_source="latest"
    )


@pytest.fixture
def ot3_local_everything(
    make_config: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(robot="ot3", monorepo_source="path", ot3_firmware_source="path")


@pytest.fixture
def ot2_remote_everything_commit_id(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(robot="ot2", monorepo_source="commit_id")


@pytest.fixture
def ot2_local_source(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(robot="ot2", monorepo_source="path")


@pytest.fixture
def heater_shaker_module_hardware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"heater-shaker-module": 1})


@pytest.fixture
def heater_shaker_module_hardware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return make_config(
        modules={"heater-shaker-module": 1}, opentrons_modules_source="path"
    )


@pytest.fixture
def heater_shaker_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    config = make_config(modules={"heater-shaker-module": 1}, monorepo_source="path")
    config["modules"][0]["emulation-level"] = EmulationLevels.FIRMWARE.value
    return config


@pytest.fixture
def heater_shaker_module_firmware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    config = make_config(modules={"heater-shaker-module": 1})
    config["modules"][0]["emulation-level"] = EmulationLevels.FIRMWARE.value
    return config


@pytest.fixture
def thermocycler_module_hardware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Hardware Thermocycler configuration for local source."""
    return make_config(
        modules={"thermocycler-module": 1}, opentrons_modules_source="path"
    )


@pytest.fixture
def thermocycler_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Firmware Thermocycler configuration for local source."""
    config = make_config(modules={"thermocycler-module": 1}, monorepo_source="path")
    config["modules"][0]["emulation-level"] = EmulationLevels.FIRMWARE.value
    return config


@pytest.fixture
def thermocycler_module_hardware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"thermocycler-module": 1})


@pytest.fixture
def thermocycler_module_firmware_remote(
    thermocycler_module_hardware_remote: Dict[str, Any],
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    thermocycler_module_hardware_remote["modules"][0][
        "emulation-level"
    ] = EmulationLevels.FIRMWARE.value
    return thermocycler_module_hardware_remote


@pytest.fixture
def temperature_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return make_config(modules={"temperature-module": 1}, monorepo_source="path")


@pytest.fixture
def temperature_module_firmware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"temperature-module": 1})


@pytest.fixture
def magnetic_module_firmware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"magnetic-module": 1})


@pytest.fixture
def magnetic_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return make_config(modules={"magnetic-module": 1}, monorepo_source="path")
