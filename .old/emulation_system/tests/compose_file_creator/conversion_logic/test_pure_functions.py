"""Tests for conversion pure functions."""

import pytest

from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.compose_file_creator.utilities.shared_functions import (
    get_build_args,
)


@pytest.mark.parametrize(
    "source_repo,source_location,format_string,head,expected_value",
    [
        [
            OpentronsRepository.OPENTRONS,
            "my-branch",
            "https://github.com/Opentrons/opentrons.git#{{branch-name}}",
            "https://github.com/Opentrons/opentrons.git#edge",
            {
                "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/opentrons.git#my-branch"
            },
        ],
        [
            OpentronsRepository.OPENTRONS_MODULES,
            "my-branch",
            "https://github.com/Opentrons/opentrons-modules.git#{{branch-name}}",
            "https://github.com/Opentrons/opentrons.git#edge",
            {
                "MODULE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/opentrons-modules.git#my-branch"
            },
        ],
        [
            OpentronsRepository.OT3_FIRMWARE,
            "my-branch",
            "https://github.com/Opentrons/ot3-firmware.git#{{branch-name}}",
            "https://github.com/Opentrons/opentrons.git#edge",
            {
                "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/ot3-firmware.git#my-branch"
            },
        ],
        [
            OpentronsRepository.OPENTRONS,
            "latest",
            "https://github.com/Opentrons/opentrons.git#{{branch-name}}",
            "https://github.com/Opentrons/opentrons.git#edge",
            {
                "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/opentrons.git#edge"
            },
        ],
        [
            OpentronsRepository.OPENTRONS_MODULES,
            "latest",
            "https://github.com/Opentrons/opentrons-modules.git#{{branch-name}}",
            "https://github.com/Opentrons/opentrons-modules.git#edge",
            {
                "MODULE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/opentrons-modules.git#edge"
            },
        ],
        [
            OpentronsRepository.OT3_FIRMWARE,
            "latest",
            "https://github.com/Opentrons/ot3-firmware.git#{{branch-name}}",
            "https://github.com/Opentrons/ot3-firmware.git#main",
            {
                "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/Opentrons/ot3-firmware.git#main"
            },
        ],
    ],
)
def test_get_build_args(
    source_repo: OpentronsRepository,
    source_location: str,
    format_string: str,
    head: str,
    expected_value: str,
) -> None:
    """Confirm that get_build_args is working as expected."""
    assert (
        get_build_args(source_repo, source_location, format_string, head)
        == expected_value
    )
