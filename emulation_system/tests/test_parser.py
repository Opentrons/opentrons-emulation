from typing import List

import pytest
import os.path
from emulation_system.src.parsers.top_level_parser import TopLevelParser
from emulation_system.src.settings_models import (
    ConfigurationSettings, DefaultFolderPaths
)
from emulation_system.src.settings import CONFIGURATION_FILE_LOCATION_VAR_NAME


# Pulled from emulation_system/tests/test_configuration.json
TEST_CONF_OPENTRONS_PATH = "/home/Documents/repos/opentrons"
TEST_CONF_FIRMWARE_PATH = "/home/Documents/repos/ot3-firmware"
TEST_CONF_MODULES_PATH = "/home/Documents/repos/opentrons-modules"

TEST_CONF_OPENTRONS_HEAD = "https://github.com/AnotherOrg/opentrons/archive/refs/heads/edge.zip"
TEST_CONF_FIRMWARE_HEAD = "https://github.com/AnotherOrg/ot3-firmware/archive/refs/heads/main.zip"
TEST_CONF_MODULES_HEAD = "https://github.com/AnotherOrg/opentrons-modules/archive/refs/heads/edge.zip"

TEST_CONF_OPENTRONS_EXPECTED_COMMIT = "https://github.com/AnotherOrg/opentrons/archive/{{commit-sha}}.zip"
TEST_CONF_FIRMWARE_EXPECTED_COMMIT = "https://github.com/AnotherOrg/ot3-firmware/archive/{{commit-sha}}.zip"
TEST_CONF_MODULES_EXPECTED_COMMIT = "https://github.com/AnotherOrg/opentrons-modules/archive/{{commit-sha}}.zip"

MADE_UP_MODULES_PATH = "/these/are/not/the/modules/you/are/looking/for"
MADE_UP_OPENTRONS_PATH = "/otie/I/am/your/father"
MADE_UP_FIRMWARE_PATH = "/the/force/is/strong/with/this/firmware"

MADE_UP_MODULES_SHA = "modulessha"
MADE_UP_OPENTRONS_SHA = "opentrons"
MADE_UP_FIRMWARE_SHA = "firmwaresha"


@pytest.fixture
def basic_dev_cmd() -> List[str]:
    return "emulator dev".split(" ")


@pytest.fixture
def complex_dev_cmd() -> List[str]:
    return (
        "em dev --detached "
        f"--opentrons-modules-repo-path={MADE_UP_MODULES_PATH} "
        f"--opentrons-repo-path={MADE_UP_OPENTRONS_PATH} "
        f"--ot3-firmware-repo-path={MADE_UP_FIRMWARE_PATH}"
    ).split(" ")


@pytest.fixture
def basic_prod_cmd() -> List[str]:
    return "emulator prod".split(" ")


@pytest.fixture
def complex_prod_cmd() -> List[str]:
    return (
        "emulator prod "
        f"--ot3-firmware-repo-sha={MADE_UP_FIRMWARE_SHA} "
        f"--opentrons-modules-repo-sha={MADE_UP_MODULES_SHA} "
        f"--opentrons-repo-sha={MADE_UP_OPENTRONS_SHA}"
    ).split(" ")


@pytest.fixture
def test_json_path() -> str:
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_configuration.json"
    )


@pytest.fixture
def test_configuration_settings(test_json_path) -> ConfigurationSettings:
    return ConfigurationSettings.from_file_path(test_json_path)


@pytest.fixture
def default_folder_paths(test_configuration_settings) -> DefaultFolderPaths:
    return test_configuration_settings.global_settings.default_folder_paths


@pytest.fixture
def set_config_file_env_var(test_json_path) -> None:
    os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME] = test_json_path
    yield
    del os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME]


def test_basic_dev_em(
        set_config_file_env_var, default_folder_paths, basic_dev_cmd
):

    args = TopLevelParser().parse(basic_dev_cmd)
    assert args.command == "emulator"
    assert args.em_command == "dev"
    assert args.detached is False
    assert args.opentrons_modules_repo_path == TEST_CONF_MODULES_PATH
    assert args.opentrons_repo_path == TEST_CONF_OPENTRONS_PATH
    assert args.ot3_firmware_repo_path == TEST_CONF_FIRMWARE_PATH


def test_complex_dev(complex_dev_cmd):
    args = TopLevelParser().parse(complex_dev_cmd)
    assert args.command == "em"
    assert args.em_command == "dev"
    assert args.detached is True
    assert args.opentrons_modules_repo_path == MADE_UP_MODULES_PATH
    assert args.opentrons_repo_path == MADE_UP_OPENTRONS_PATH
    assert args.ot3_firmware_repo_path == MADE_UP_FIRMWARE_PATH


def test_basic_prod_em(basic_prod_cmd):
    args = TopLevelParser().parse(basic_prod_cmd)
    assert args.command == "emulator"
    assert args.em_command == "prod"
    assert args.detached is False
    assert args.ot3_firmware_repo_sha == "latest"
    assert args.opentrons_modules_repo_sha == "latest"
    assert args.opentrons_repo_sha == "latest"



def test_complex_prod_em(complex_prod_cmd):
    args = TopLevelParser().parse(complex_prod_cmd)
    assert args.command == "emulator"
    assert args.em_command == "prod"
    assert args.detached is False
    assert args.ot3_firmware_repo_sha == MADE_UP_FIRMWARE_SHA
    assert args.opentrons_modules_repo_sha == MADE_UP_MODULES_SHA
    assert args.opentrons_repo_sha == MADE_UP_OPENTRONS_SHA

