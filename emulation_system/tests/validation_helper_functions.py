from typing import Any, Dict, Optional, cast

from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.images import (
    HeaterShakerModuleImages,
    MagneticModuleImages,
    RobotServerImage,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)
from tests.compose_file_creator.conftest import (
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)

CONTAINER_NAME_TO_IMAGE = {
    OT2_ID: RobotServerImage().image_name,
    f"{THERMOCYCLER_MODULE_ID}-1": ThermocyclerModuleImages().hardware_image_name,
    f"{HEATER_SHAKER_MODULE_ID}-1": HeaterShakerModuleImages().hardware_image_name,
    f"{TEMPERATURE_MODULE_ID}-1": TemperatureModuleImages().firmware_image_name,
    f"{MAGNETIC_MODULE_ID}-1": MagneticModuleImages().firmware_image_name,
}
SERVICE_NAMES = [
    OT2_ID,
    f"{THERMOCYCLER_MODULE_ID}-1",
    f"{HEATER_SHAKER_MODULE_ID}-1",
    f"{TEMPERATURE_MODULE_ID}-1",
    f"{MAGNETIC_MODULE_ID}-1",
]
EXTRA_MOUNT_PATH = "/var/log/log_files"


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


def get_env(container: Service) -> Dict[str, Any] | None:
    return (
        None
        if container.environment is None
        else cast(Dict[str, Any], container.environment.__root__)
    )
