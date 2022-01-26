"""Function useful to multiple service creation modules."""
from typing import (
    List,
    Optional,
    Union,
    cast,
)

from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.compose_file_model import (
    BuildItem,
    Volume1,
)
from emulation_system.compose_file_creator.settings.custom_types import Containers
from emulation_system.consts import DOCKERFILE_DIR_LOCATION


def generate_container_name(
    container_id: str, config_model: SystemConfigurationModel
) -> str:
    """If system-unique-id is defined prefix it to container name."""
    return (
        f"{config_model.system_unique_id}-{container_id}"
        if config_model.system_unique_id is not None
        else container_id
    )


def get_service_build(image_name: str) -> BuildItem:
    """Generate BuildItem object for Service."""
    return BuildItem(context=DOCKERFILE_DIR_LOCATION, target=image_name)


def get_service_image(image_name: str) -> str:
    """Build image string."""
    return f"{image_name}:latest"


def get_mount_strings(container: Containers) -> Optional[List[Union[str, Volume1]]]:
    """Get mount strings defined on container."""
    mount_strings = container.get_mount_strings()
    return (
        cast(List[Union[str, Volume1]], mount_strings)
        if len(mount_strings) > 0
        else None
    )
