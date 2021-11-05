from emulation_system.src.parsers.top_level_parser import TopLevelParser
from emulation_system.tests.conftest import (
    BASIC_DEV_CMDS_TO_RUN,
    COMPLEX_DEV_COMMANDS_TO_RUN,
    BASIC_PROD_COMMANDS_TO_RUN,
    COMPLEX_PROD_COMMANDS_TO_RUN
)


def test_basic_dev_em_commands(set_config_file_env_var, basic_dev_cmd):
    dev_em_creator = TopLevelParser().parse(basic_dev_cmd)
    assert dev_em_creator.get_commands() == BASIC_DEV_CMDS_TO_RUN


def test_complex_dev_em_commands(set_config_file_env_var, complex_dev_cmd):
    dev_em_creator = TopLevelParser().parse(complex_dev_cmd)
    assert dev_em_creator.get_commands() == COMPLEX_DEV_COMMANDS_TO_RUN


def test_basic_prod_em_commands(set_config_file_env_var, basic_prod_cmd):
    prod_em_creator = TopLevelParser().parse(basic_prod_cmd)
    assert prod_em_creator.get_commands() == BASIC_PROD_COMMANDS_TO_RUN


def test_complex_prod_em_commands(set_config_file_env_var, complex_prod_cmd):
    prod_em_creator = TopLevelParser().parse(complex_prod_cmd)
    assert prod_em_creator.get_commands() == COMPLEX_PROD_COMMANDS_TO_RUN
