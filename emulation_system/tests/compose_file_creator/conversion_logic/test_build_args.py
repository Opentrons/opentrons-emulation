"""Tests for conversion pure functions."""
from typing import Dict, Type, Union

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.source import (
    MonorepoSource,
    OpentronsModulesSource,
    OT3FirmwareSource,
)


@pytest.mark.parametrize(
    "source, source_location, expected_value",
    [
        [
            MonorepoSource,
            "latest",
            {
                "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/opentrons.git#edge"
            },
        ],
        [
            MonorepoSource,
            "edge",
            {
                "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/opentrons.git#edge"
            },
        ],
        [MonorepoSource, lazy_fixture("opentrons_dir"), None],
        [
            OpentronsModulesSource,
            "latest",
            {
                "MODULE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/opentrons-modules.git#edge"
            },
        ],
        [
            OpentronsModulesSource,
            "edge",
            {
                "MODULE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/opentrons-modules.git#edge"
            },
        ],
        [OpentronsModulesSource, lazy_fixture("opentrons_modules_dir"), None],
        [
            OT3FirmwareSource,
            "latest",
            {
                "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/ot3-firmware.git#main"
            },
        ],
        [
            OT3FirmwareSource,
            "main",
            {
                "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/ot3-firmware.git#main"
            },
        ],
        [OT3FirmwareSource, lazy_fixture("ot3_firmware_dir"), None],
    ],
)
def test_get_build_args(
    source: Type[Union[MonorepoSource, OpentronsModulesSource, OT3FirmwareSource]],
    source_location: str,
    expected_value: Dict[str, str] | None,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm that get_build_args is working as expected."""
    source_obj = source(source_location=source_location)
    assert source_obj.generate_build_args(testing_global_em_config) == expected_value
