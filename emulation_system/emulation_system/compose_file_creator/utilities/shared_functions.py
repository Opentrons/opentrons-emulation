"""Function useful to multiple service creation modules."""
from typing import List

from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
    RepoToBuildArgMapping,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
)


def get_build_args(
    source_repo: OpentronsRepository,
    source_location: str,
    format_string: str,
    head: str,
) -> IntermediateBuildArgs:
    """Get build arguments for service."""
    env_var_to_use = str(RepoToBuildArgMapping[source_repo.name].value)
    value = (
        head
        if source_location == "latest"
        else format_string.replace("{{commit-sha}}", source_location)
    )
    return {env_var_to_use: value}


def _add_named_volumes(
    mount_list: List[str],
    directory_to_search_for: str,
    build_dirs: List[str],
) -> None:
    """Adds named volumes for build files."""
    for mount in mount_list:
        if directory_to_search_for in mount:
            mount_list.extend(build_dirs)
            return


def add_ot3_firmware_named_volumes(mount_list: List[str]) -> None:
    """Add ot3 firmware named volumes."""
    _add_named_volumes(
        mount_list,
        "/ot3-firmware",
        [
            "ot3-firmware-build-host:/ot3-firmware/build-host",
            "ot3-firmware-stm32-tools:/ot3-firmware/stm32-tools",
        ],
    )


def add_opentrons_named_volumes(mount_list: List[str]) -> None:
    """Add opentrons named volumes."""
    _add_named_volumes(
        mount_list,
        "/opentrons",
        ["opentrons-python-dist:/dist"],
    )


def add_opentrons_modules_named_volumes(mount_list: List[str]) -> None:
    """Add opentrons-modules named volumes."""
    _add_named_volumes(
        mount_list,
        "/opentrons-modules",
        [
            "opentrons-modules-build-stm32-host:/opentrons-modules/build-stm32-host",
            "opentrons-modules-stm32-tools:/opentrons-modules/stm32-tools",
        ],
    )

def to_kebab(string: str) -> str:
    """Converts snake case formatted string to kebab case."""
    return string.replace("_", "-")
