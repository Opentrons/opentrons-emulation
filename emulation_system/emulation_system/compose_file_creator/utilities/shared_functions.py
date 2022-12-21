"""Function useful to multiple service creation modules."""

from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from emulation_system.source import Source


def get_build_args(
    source: Source, global_settings: OpentronsEmulationConfiguration
) -> IntermediateBuildArgs | None:
    """Get build arguments for service."""

    if source.is_local():
        return None

    env_var_to_use = str(source.repo_to_build_arg_mapping.value)
    head = global_settings.get_repo_head(source.repo)
    format_string = global_settings.get_repo_commit(source.repo)
    source_location = source.source_location
    value = (
        head
        if source_location == "latest"
        else format_string.replace("{{commit-sha}}", source_location)
    )
    return {env_var_to_use: value}


def to_kebab(string: str) -> str:
    return string.replace("_", "-")
