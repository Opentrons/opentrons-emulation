"""Tests for conversion pure functions."""
from typing import Dict, Type, Union

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator.utilities.shared_functions import (
    get_build_args,
)
from emulation_system.source import (
    MonorepoSource,
    OpentronsModulesSource,
    OT3FirmwareSource,
)
from tests.conftest import FAKE_COMMIT_ID


@pytest.mark.parametrize(
    "source, source_location, expected_value",
    [
        [
            MonorepoSource,
            "latest",
            {
                "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/opentrons/archive/refs/heads/edge.zip"
            },
        ],
        [
            MonorepoSource,
            FAKE_COMMIT_ID,
            {
                "OPENTRONS_SOURCE_DOWNLOAD_LOCATION": f"https://github.com/AnotherOrg/opentrons/archive/{FAKE_COMMIT_ID}.zip"
            },
        ],
        [MonorepoSource, lazy_fixture("opentrons_dir"), None],
        [
            OpentronsModulesSource,
            "latest",
            {
                "MODULE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/opentrons-modules/archive/refs/heads/edge.zip"
            },
        ],
        [
            OpentronsModulesSource,
            FAKE_COMMIT_ID,
            {
                "MODULE_SOURCE_DOWNLOAD_LOCATION": f"https://github.com/AnotherOrg/opentrons-modules/archive/{FAKE_COMMIT_ID}.zip"
            },
        ],
        [OpentronsModulesSource, lazy_fixture("opentrons_modules_dir"), None],
        [
            OT3FirmwareSource,
            "latest",
            {
                "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": "https://github.com/AnotherOrg/ot3-firmware/archive/refs/heads/main.zip"
            },
        ],
        [
            OT3FirmwareSource,
            FAKE_COMMIT_ID,
            {
                "FIRMWARE_SOURCE_DOWNLOAD_LOCATION": f"https://github.com/AnotherOrg/ot3-firmware/archive/{FAKE_COMMIT_ID}.zip"
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
    assert get_build_args(source_obj, testing_global_em_config) == expected_value
