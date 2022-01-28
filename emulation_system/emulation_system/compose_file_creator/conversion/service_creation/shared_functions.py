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
    ListOrDict,
    Volume1,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.compose_file_creator.settings.custom_types import Containers
from emulation_system.consts import DOCKERFILE_DIR_LOCATION
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)

REPO_TO_BUILD_ARG_MAPPING = {
    OpentronsRepository.OPENTRONS: "OPENTRONS_SOURCE_DOWNLOAD_LOCATION",
    OpentronsRepository.OPENTRONS_MODULES: "MODULE_SOURCE_DOWNLOAD_LOCATION",
    OpentronsRepository.OT3_FIRMWARE: "FIRMWARE_SOURCE_DOWNLOAD_LOCATION",
}

def generate_container_name(
    container_id: str, config_model: SystemConfigurationModel
) -> str:
    """If system-unique-id is defined prefix it to container name."""
    return (
        f"{config_model.system_unique_id}-{container_id}"
        if config_model.system_unique_id is not None
        else container_id
    )


def get_service_build(image_name: str, build_args: Optional[ListOrDict]) -> BuildItem:
    """Generate BuildItem object for Service."""
    return BuildItem(
        context=DOCKERFILE_DIR_LOCATION, target=image_name, args=build_args
    )


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

def get_build_args(
    source_repo: OpentronsRepository,
    source_location: str,
    global_settings: OpentronsEmulationConfiguration,
) -> ListOrDict:


    REPO_TO_COMMIT_FORMAT_STRING_MAPPING = {
        OpentronsRepository.OPENTRONS: global_settings.emulation_settings.source_download_locations.commits.opentrons,  # noqa: E501
        OpentronsRepository.OPENTRONS_MODULES: global_settings.emulation_settings.source_download_locations.commits.modules,  # noqa: E501
        OpentronsRepository.OT3_FIRMWARE: global_settings.emulation_settings.source_download_locations.commits.ot3_firmware,  # noqa: E501
    }
    env_var_to_use = REPO_TO_BUILD_ARG_MAPPING[source_repo]
    commit_format_string_to_use = REPO_TO_COMMIT_FORMAT_STRING_MAPPING[source_repo]
    arg_dict = {
        env_var_to_use: commit_format_string_to_use.replace(
            "{{commit-sha}}", source_location
        )
    }
    return ListOrDict(__root__=arg_dict)
