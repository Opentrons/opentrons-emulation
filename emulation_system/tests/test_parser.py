from typing import List

import pytest
import os.path

from command_creators.command import CommandList, Command
from emulation_system.src.parsers.top_level_parser import TopLevelParser
from emulation_system.src.settings_models import (
    ConfigurationSettings, DefaultFolderPaths
)
from emulation_system.src.settings import CONFIGURATION_FILE_LOCATION_VAR_NAME
from emulation_system.src.command_creators.emulation_creator import (
    EmulationCreatorMixin,
    ProdEmulationCreator,
    DevEmulationCreator
)


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

BASIC_DEV_CMDS_TO_RUN = CommandList(
    [
        Command(
            EmulationCreatorMixin.CLEAN_COMMAND_NAME,
            "docker-compose -f docker-compose-dev.yaml kill "
            "&& docker-compose -f docker-compose-dev.yaml rm -f"
        ),
        Command(
            EmulationCreatorMixin.BUILD_COMMAND_NAME,
            (
                "COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_BUILDKIT=1 "
                "OT3_FIRMWARE_DIRECTORY=/home/Documents/repos/ot3-firmware "
                "OPENTRONS_MODULES_DIRECTORY=/home/Documents/repos/opentrons-modules "
                "OPENTRONS_DIRECTORY=/home/Documents/repos/opentrons "
                "docker-compose --verbose -f docker-compose-dev.yaml build"
            )
        ),
        Command(
            EmulationCreatorMixin.RUN_COMMAND_NAME,
            (
                "OT3_FIRMWARE_DIRECTORY=/home/Documents/repos/ot3-firmware "
                "OPENTRONS_MODULES_DIRECTORY=/home/Documents/repos/opentrons-modules "
                "OPENTRONS_DIRECTORY=/home/Documents/repos/opentrons "
                "docker-compose -f docker-compose-dev.yaml up "
            )
        )
    ]
)


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

    dev_em_creator = TopLevelParser().parse(basic_dev_cmd)
    assert dev_em_creator.detached is False
    assert dev_em_creator.modules_path == TEST_CONF_MODULES_PATH
    assert dev_em_creator.opentrons_path == TEST_CONF_OPENTRONS_PATH
    assert dev_em_creator.ot3_firmware_path == TEST_CONF_FIRMWARE_PATH


def test_complex_dev(set_config_file_env_var, complex_dev_cmd):
    dev_em_creator = TopLevelParser().parse(complex_dev_cmd)
    assert dev_em_creator.detached is True
    assert dev_em_creator.modules_path == MADE_UP_MODULES_PATH
    assert dev_em_creator.opentrons_path == MADE_UP_OPENTRONS_PATH
    assert dev_em_creator.ot3_firmware_path == MADE_UP_FIRMWARE_PATH


def test_basic_prod_em(set_config_file_env_var, basic_prod_cmd):
    prod_em_creator = TopLevelParser().parse(basic_prod_cmd)
    assert prod_em_creator.detached is False
    assert prod_em_creator.ot3_firmware_download_location == TEST_CONF_FIRMWARE_HEAD
    assert prod_em_creator.modules_download_location == TEST_CONF_MODULES_HEAD
    assert prod_em_creator.opentrons_download_location == TEST_CONF_OPENTRONS_HEAD


def test_complex_prod_em(set_config_file_env_var, complex_prod_cmd):
    prod_em_creator = TopLevelParser().parse(complex_prod_cmd)
    assert prod_em_creator.detached is False
    assert prod_em_creator.ot3_firmware_download_location == \
           TEST_CONF_FIRMWARE_EXPECTED_COMMIT.replace(
               "{{commit-sha}}", MADE_UP_FIRMWARE_SHA
           )
    assert prod_em_creator.modules_download_location == \
           TEST_CONF_MODULES_EXPECTED_COMMIT.replace(
               "{{commit-sha}}", MADE_UP_MODULES_SHA
           )
    assert prod_em_creator.opentrons_download_location == \
           TEST_CONF_OPENTRONS_EXPECTED_COMMIT.replace(
               "{{commit-sha}}", MADE_UP_OPENTRONS_SHA
           )


def test_basic_dev_em_commands(set_config_file_env_var, basic_dev_cmd):
    dev_em_creator = TopLevelParser().parse(basic_dev_cmd)
    assert dev_em_creator.get_commands() == BASIC_DEV_CMDS_TO_RUN
