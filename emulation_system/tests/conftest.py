"""Utilities for emulation_system tests."""
import os

import pytest

from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
    SourceDownloadLocations,
)


def get_test_conf() -> OpentronsEmulationConfiguration:
    """Returns configuration settings from test config file."""
    return OpentronsEmulationConfiguration.from_file_path(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_configuration.json"
        )
    )


def get_source_download_locations() -> SourceDownloadLocations:
    """Get source download locations from test config file."""
    return get_test_conf().emulation_settings.source_download_locations


def get_head(name: str) -> str:
    """Get head download location for repo from test config file."""
    return get_source_download_locations().heads.__getattribute__(
        name.replace("-", "_")
    )


def get_commit(name: str) -> str:
    """Get commit format string download location for repo from test config file."""
    return get_source_download_locations().commits.__getattribute__(
        name.replace("-", "_")
    )


TEST_CONF_OPENTRONS_HEAD = get_head("opentrons")
TEST_CONF_FIRMWARE_HEAD = get_head("ot3-firmware")
TEST_CONF_MODULES_HEAD = get_head("modules")

TEST_CONF_OPENTRONS_EXPECTED_COMMIT = get_commit("opentrons")
TEST_CONF_FIRMWARE_EXPECTED_COMMIT = get_commit("ot3-firmware")
TEST_CONF_MODULES_EXPECTED_COMMIT = get_commit("modules")


@pytest.fixture
def testing_global_em_config() -> OpentronsEmulationConfiguration:
    """Get test configuration of OpentronsEmulationConfiguration."""
    return get_test_conf()
