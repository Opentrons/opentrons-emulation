from emulation_system.src.parsers.top_level_parser import TopLevelParser
from emulation_system.tests.conftest import (
    TEST_CONF_FIRMWARE_PATH, MADE_UP_OPENTRONS_PATH, MADE_UP_FIRMWARE_PATH,
    TEST_CONF_FIRMWARE_HEAD, TEST_CONF_MODULES_HEAD, EXPECTED_FIRMWARE_COMMIT,
    EXPECTED_MODULES_COMMIT, EXPECTED_OPENTRONS_COMMIT, TEST_CONF_MODULES_PATH,
    TEST_CONF_OPENTRONS_PATH, MADE_UP_MODULES_PATH, TEST_CONF_OPENTRONS_HEAD,
)


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
    assert prod_em_creator.detached is True
    assert prod_em_creator.ot3_firmware_download_location == EXPECTED_FIRMWARE_COMMIT

    assert prod_em_creator.modules_download_location == EXPECTED_MODULES_COMMIT

    assert prod_em_creator.opentrons_download_location == EXPECTED_OPENTRONS_COMMIT
