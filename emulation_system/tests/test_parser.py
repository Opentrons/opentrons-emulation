import pytest
import os.path
from emulation_system.src.parsers.top_level_parser import TopLevelParser
from emulation_system.src.settings_models import ConfigurationSettings
from emulation_system.src.settings import CONFIGURATION_FILE_LOCATION_VAR_NAME


MADE_UP_MODULES_PATH = "/these/are/not/the/modules/you/are/looking/for"
MADE_UP_OPENTRONS_PATH = "/otie/I/am/your/father"
MADE_UP_FIRMWARE_PATH = "/the/force/is/strong/with/this/firmware"


@pytest.fixture
def basic_dev_cmd():
    return "emulator dev".split(" ")


@pytest.fixture
def complex_dev_cmd():
    return (
        "em dev --detached "
        f"--opentrons-modules-repo-path={MADE_UP_MODULES_PATH} "
        f"--opentrons-repo-path={MADE_UP_OPENTRONS_PATH} "
        f"--ot3-firmware-repo-path={MADE_UP_FIRMWARE_PATH}"
    ).split(" ")


@pytest.fixture
def test_json_path():
    return os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "test_configuration.json"
    )


@pytest.fixture
def test_configuration_settings(test_json_path):
    return ConfigurationSettings.from_file_path(test_json_path)


@pytest.fixture
def default_folder_paths(test_configuration_settings):
    return test_configuration_settings.global_settings.default_folder_paths


@pytest.fixture
def set_config_file_env_var(test_json_path):

    os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME] = test_json_path
    yield
    del os.environ[CONFIGURATION_FILE_LOCATION_VAR_NAME]


@pytest.fixture
def parser():
    return TopLevelParser()


def test_basic_dev_em(
        set_config_file_env_var, parser, default_folder_paths, basic_dev_cmd
):

    args = parser.parse(basic_dev_cmd)
    assert args.command == "emulator"
    assert args.detached is False
    assert args.opentrons_modules_repo_path == default_folder_paths.modules
    assert args.opentrons_repo_path == default_folder_paths.opentrons
    assert args.ot3_firmware_repo_path == default_folder_paths.ot3_firmware


def test_complex_dev(parser, complex_dev_cmd):
    args = parser.parse(complex_dev_cmd)
    assert args.command == "em"
    assert args.detached is True
    assert args.opentrons_modules_repo_path == MADE_UP_MODULES_PATH
    assert args.opentrons_repo_path == MADE_UP_OPENTRONS_PATH
    assert args.ot3_firmware_repo_path == MADE_UP_FIRMWARE_PATH

