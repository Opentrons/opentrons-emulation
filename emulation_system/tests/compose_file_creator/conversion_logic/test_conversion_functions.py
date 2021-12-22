"""Tests for confirming returned image names are correct."""
from typing import Union

import pytest

from emulation_system.compose_file_creator.conversion_logic.conversion_functions import (  # noqa: E501
    get_image_name,
    get_image_name_from_hardware_model,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    EmulationLevels,
    Hardware,
    SourceType,
)

CONFIGURATIONS = [
    # OT2
    [Hardware.OT2, EmulationLevels.HARDWARE, SourceType.LOCAL, None],
    [Hardware.OT2, EmulationLevels.HARDWARE, SourceType.REMOTE, None],
    [Hardware.OT2, EmulationLevels.FIRMWARE, SourceType.LOCAL, "robot-server-local"],
    [Hardware.OT2, EmulationLevels.FIRMWARE, SourceType.REMOTE, "robot-server-remote"],
    # Heater Shaker Module
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.LOCAL,
        "heater-shaker-hardware-local",
    ],
    [
        Hardware.HEATER_SHAKER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.REMOTE,
        "heater-shaker-hardware-remote",
    ],
    [Hardware.HEATER_SHAKER_MODULE, EmulationLevels.FIRMWARE, SourceType.LOCAL, None],
    [Hardware.HEATER_SHAKER_MODULE, EmulationLevels.FIRMWARE, SourceType.REMOTE, None],
    # Temperature Module
    [Hardware.TEMPERATURE_MODULE, EmulationLevels.HARDWARE, SourceType.LOCAL, None],
    [Hardware.TEMPERATURE_MODULE, EmulationLevels.HARDWARE, SourceType.REMOTE, None],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "tempdeck-firmware-local",
    ],
    [
        Hardware.TEMPERATURE_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "tempdeck-firmware-remote",
    ],
    # Thermocycler Module
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.LOCAL,
        "thermocycler-hardware-local",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.HARDWARE,
        SourceType.REMOTE,
        "thermocycler-hardware-remote",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "thermocycler-firmware-local",
    ],
    [
        Hardware.THERMOCYCLER_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "thermocycler-firmware-remote",
    ],
    # Magnetic Module
    [Hardware.MAGNETIC_MODULE, EmulationLevels.HARDWARE, SourceType.LOCAL, None],
    [Hardware.MAGNETIC_MODULE, EmulationLevels.HARDWARE, SourceType.REMOTE, None],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.LOCAL,
        "magdeck-firmware-local",
    ],
    [
        Hardware.MAGNETIC_MODULE,
        EmulationLevels.FIRMWARE,
        SourceType.REMOTE,
        "magdeck-firmware-remote",
    ],
]


@pytest.mark.parametrize(
    "hardware_name,emulation_level,source_type,expected_name", CONFIGURATIONS
)
def test_get_image_name(
    hardware_name: Hardware,
    emulation_level: EmulationLevels,
    source_type: SourceType,
    expected_name: Union[str, None],
) -> None:
    """Test that correct image name is returned by get_image_name."""
    assert get_image_name(hardware_name, emulation_level, source_type) == expected_name


def test_get_image_name_from_hardware_model() -> None:
    """Test that get_image_name_from_hardware_model returns correct value."""
    model = HeaterShakerModuleInputModel(
        id="my-heater-shaker",
        hardware=Hardware.HEATER_SHAKER_MODULE,
        source_type=SourceType.REMOTE,
        source_location="latest",
        emulation_level=EmulationLevels.HARDWARE,
    )
    assert get_image_name_from_hardware_model(model) == "heater-shaker-hardware-remote"
