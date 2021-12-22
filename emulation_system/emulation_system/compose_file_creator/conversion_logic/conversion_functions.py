"""Functions used for converting from input file to Docker Compose File.

These functions should be called by the Converter object
"""

from typing import (
    Optional,
    Union,
)

from emulation_system.compose_file_creator.input.hardware_models.hardware_model import (
    HardwareModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    ExtraMount,
    Hardware,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import IMAGE_MAPPING


def get_image_name(
    hardware_name: Union[Hardware, str],
    emulation_level: EmulationLevels,
    source_type: SourceType,
) -> Optional[str]:
    """Get image name to run based off of passed parameters."""
    image = IMAGE_MAPPING[hardware_name]
    comp_tuple = (source_type, emulation_level)

    if comp_tuple == (SourceType.REMOTE, EmulationLevels.HARDWARE):
        image_name = image.remote_hardware_image_name
    elif comp_tuple == (SourceType.REMOTE, EmulationLevels.FIRMWARE):
        image_name = image.remote_firmware_image_name
    elif comp_tuple == (SourceType.LOCAL, EmulationLevels.HARDWARE):
        image_name = image.local_hardware_image_name
    else:  # (SourceType.LOCAL, EmulationLevels.FIRMWARE)
        image_name = image.local_firmware_image_name

    return image_name


def get_image_name_from_hardware_model(hardware_model: HardwareModel) -> Optional[str]:
    """Convenience function to get image name by passing HardwareModel object.

    Calls get_image_name under the hood.
    """
    return get_image_name(
        hardware_model.hardware,
        hardware_model.emulation_level,
        hardware_model.source_type,
    )


def get_bind_mount_string(mount: ExtraMount) -> str:
    """Return bind mount string to add compose file."""
    return f"${{{mount.name}}}:{mount.mount_path}"
