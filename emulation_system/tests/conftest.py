"""Utilities for emulation_system tests."""
import os
from typing import Generator

import pytest
from emulation_system.consts import CONFIGURATION_FILE_LOCATION_VAR_NAME
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
    DefaultFolderPaths,
    SourceDownloadLocations,
)


def get_test_configuration_file_path() -> str:
    """Returns path to test file."""
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_configuration.json"
    )


def get_test_resources_dir() -> str:
    """Get path to test_resources directory."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_resources")


@pytest.fixture
def json_for_testing_path() -> str:
    """Returns path to test file."""
    return get_test_configuration_file_path()


def get_test_conf() -> OpentronsEmulationConfiguration:
    """Returns configuration settings from test config file."""
    return OpentronsEmulationConfiguration.from_file_path(
        get_test_configuration_file_path()
    )


def get_default_folder_path(name: str) -> str:
    """Gets default folder path from test config file."""
    return get_test_conf().global_settings.default_folder_paths.__getattribute__(
        name.replace("-", "_")
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


TEST_CONF_OPENTRONS_PATH = get_default_folder_path("opentrons")
TEST_CONF_FIRMWARE_PATH = get_default_folder_path("ot3-firmware")
TEST_CONF_MODULES_PATH = get_default_folder_path("modules")

TEST_CONF_OPENTRONS_HEAD = get_head("opentrons")
TEST_CONF_FIRMWARE_HEAD = get_head("ot3-firmware")
TEST_CONF_MODULES_HEAD = get_head("modules")

TEST_CONF_OPENTRONS_EXPECTED_COMMIT = get_commit("opentrons")
TEST_CONF_FIRMWARE_EXPECTED_COMMIT = get_commit("ot3-firmware")
TEST_CONF_MODULES_EXPECTED_COMMIT = get_commit("modules")


@pytest.fixture
def default_folder_paths() -> DefaultFolderPaths:
    """Returns default folder paths from test configuration file."""
    return get_test_conf().global_settings.default_folder_paths


@pytest.fixture
def set_config_file_env_var(json_for_testing_path: str) -> Generator:
    """Sets configuration file location env var then removes it after test."""
    os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME] = json_for_testing_path
    yield
    del os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME]
