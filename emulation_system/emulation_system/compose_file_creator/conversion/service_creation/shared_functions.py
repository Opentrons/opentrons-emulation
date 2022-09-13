"""Function useful to multiple service creation modules."""
import pathlib
from typing import Any, Dict, List, Optional, Union, cast

from emulation_system import SystemConfigurationModel
from emulation_system.compose_file_creator import BuildItem
from emulation_system.compose_file_creator.input.hardware_models import RobotInputModel
from emulation_system.compose_file_creator.output.compose_file_model import (
    ListOrDict,
    Volume1,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    ENTRYPOINT_MOUNT_NAME,
    FileMount,
    MountTypes,
    OpentronsRepository,
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.settings.custom_types import Containers
from emulation_system.consts import (
    DEV_DOCKERFILE_NAME,
    DOCKERFILE_DIR_LOCATION,
    DOCKERFILE_NAME,
    ENTRYPOINT_FILE_LOCATION,
)


def generate_container_name(
    container_id: str, config_model: SystemConfigurationModel
) -> str:
    """If system-unique-id is defined prefix it to container name."""
    return (
        f"{config_model.system_unique_id}-{container_id}"
        if config_model.system_unique_id is not None
        else container_id
    )


def get_service_build(
    image_name: str, build_args: Optional[ListOrDict], dev: bool
) -> BuildItem:
    """Generate BuildItem object for Service."""
    return BuildItem(
        context=DOCKERFILE_DIR_LOCATION,
        target=image_name,
        args=build_args,
        dockerfile=get_dockerfile_name(dev),
    )


def get_service_image(image_name: str) -> str:
    """Build image string."""
    return f"{image_name}:latest"


def get_mount_strings(container: Containers) -> Optional[List[Union[str, Volume1]]]:
    """Get mount strings defined on container."""
    mount_strings = (
        container.get_robot_server_mount_strings()
        if issubclass(container.__class__, RobotInputModel)
        else container.get_mount_strings()
    )
    if len(mount_strings) > 0:
        mount_strings.append(get_entrypoint_mount_string())
        if container.get_source_repo() == OpentronsRepository.OPENTRONS:
            add_opentrons_named_volumes(cast(List[Union[str, Volume1]], mount_strings))
        elif container.get_source_repo() == OpentronsRepository.OPENTRONS_MODULES:
            add_opentrons_modules_named_volumes(
                cast(List[Union[str, Volume1]], mount_strings)
            )
        elif container.get_source_repo() == OpentronsRepository.OT3_FIRMWARE:
            add_ot3_firmware_named_volumes(
                cast(List[Union[str, Volume1]], mount_strings)
            )
        return cast(List[Union[str, Volume1]], mount_strings)
    else:
        return None


def get_entrypoint_mount_string() -> str:
    """Return bind mount string to entrypoint.sh."""
    return FileMount(
        name=ENTRYPOINT_MOUNT_NAME,
        type=MountTypes.FILE,
        source_path=pathlib.Path(ENTRYPOINT_FILE_LOCATION),
        mount_path="/entrypoint.sh",
    ).get_bind_mount_string()


def get_build_args(
    source_repo: OpentronsRepository,
    source_location: str,
    format_string: str,
    head: str,
) -> ListOrDict:
    """Get build arguments for service."""
    env_var_to_use = RepoToBuildArgMapping[source_repo.name]
    value = (
        head
        if source_location == "latest"
        else format_string.replace("{{commit-sha}}", source_location)
    )
    arg_dict: Dict[str, Any] = {env_var_to_use: value}
    return ListOrDict(__root__=arg_dict)


def _add_named_volumes(
    mount_list: List[Union[str, Volume1]],
    directory_to_search_for: str,
    build_dirs: List[str],
) -> None:
    """Adds named volumes for build files."""
    for mount in mount_list:
        if directory_to_search_for in mount:
            mount_list.extend(build_dirs)
            break


def add_ot3_firmware_named_volumes(mount_list: List[Union[str, Volume1]]) -> None:
    """Add ot3 firmware named volumes."""
    _add_named_volumes(
        mount_list,
        "/ot3-firmware",
        [
            "ot3-firmware-build-host:/ot3-firmware/build-host",
            "ot3-firmware-stm32-tools:/ot3-firmware/stm32-tools",
        ],
    )


def add_opentrons_named_volumes(mount_list: List[Union[str, Volume1]]) -> None:
    """Add opentrons named volumes."""
    _add_named_volumes(
        mount_list,
        "/opentrons",
        ["opentrons-python-dist:/dist"],
    )


def add_opentrons_modules_named_volumes(mount_list: List[Union[str, Volume1]]) -> None:
    """Add opentrons-modules named volumes."""
    _add_named_volumes(
        mount_list,
        "/opentrons-modules",
        [
            "opentrons-modules-build-stm32-host:/opentrons-modules/build-stm32-host",
            "opentrons-modules-stm32-tools:/opentrons-modules/stm32-tools",
        ],
    )


def get_dockerfile_name(dev: bool) -> str:
    """Get dockerfile name based off of --dev option."""
    return DEV_DOCKERFILE_NAME if dev else DOCKERFILE_NAME
