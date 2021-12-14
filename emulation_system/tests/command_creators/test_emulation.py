"""Tests for emulation command."""
from typing import List, Generator

import pytest

from emulation_system.parsers.top_level_parser import TopLevelParser
from tests.emulation_conftest import (
    BASIC_DEV_CMDS_TO_RUN,
    COMPLEX_DEV_COMMANDS_TO_RUN,
    BASIC_PROD_COMMANDS_TO_RUN,
    COMPLEX_PROD_COMMANDS_TO_RUN,
    MADE_UP_MODULES_PATH,
    MADE_UP_OPENTRONS_PATH,
    MADE_UP_FIRMWARE_PATH,
    MADE_UP_FIRMWARE_SHA,
    MADE_UP_MODULES_SHA,
    MADE_UP_OPENTRONS_SHA,
)


@pytest.fixture
def basic_emulation_dev_cmd() -> List[str]:
    """Create most basic dev emulation command."""
    return "emulator dev".split(" ")


@pytest.fixture
def complex_emulation_dev_cmd() -> List[str]:
    """Create complex dev emulation command with all options specified."""
    return (
        "em dev --detached "
        f"--opentrons-modules-repo-path={MADE_UP_MODULES_PATH} "
        f"--opentrons-repo-path={MADE_UP_OPENTRONS_PATH} "
        f"--ot3-firmware-repo-path={MADE_UP_FIRMWARE_PATH}"
    ).split(" ")


@pytest.fixture
def basic_prod_emulation_cmd() -> List[str]:
    """Create basic emulation dev command."""
    return "emulator prod".split(" ")


@pytest.fixture
def complex_prod_emulation_cmd() -> List[str]:
    """Create complex prod emulation command with all options specified."""
    return (
        "emulator prod --detached "
        f"--ot3-firmware-repo-sha={MADE_UP_FIRMWARE_SHA} "
        f"--opentrons-modules-repo-sha={MADE_UP_MODULES_SHA} "
        f"--opentrons-repo-sha={MADE_UP_OPENTRONS_SHA}"
    ).split(" ")


def test_basic_dev_em_commands(
    set_config_file_env_var: Generator, basic_emulation_dev_cmd: List[str]
) -> None:
    """Confirm that basic dev emulation command is parsed correctly."""
    dev_em_creator = TopLevelParser().parse(basic_emulation_dev_cmd)
    assert dev_em_creator.get_commands() == BASIC_DEV_CMDS_TO_RUN


def test_complex_dev_em_commands(
    set_config_file_env_var: Generator, complex_emulation_dev_cmd: List[str]
) -> None:
    """Confirm that complex dev emulation command is parsed correctly."""
    dev_em_creator = TopLevelParser().parse(complex_emulation_dev_cmd)
    assert dev_em_creator.get_commands() == COMPLEX_DEV_COMMANDS_TO_RUN


def test_basic_prod_em_commands(
    set_config_file_env_var: Generator, basic_prod_emulation_cmd: List[str]
) -> None:
    """Confirm that basic prod emulation command is parsed correctly."""
    prod_em_creator = TopLevelParser().parse(basic_prod_emulation_cmd)
    assert prod_em_creator.get_commands() == BASIC_PROD_COMMANDS_TO_RUN


def test_complex_prod_em_commands(
    set_config_file_env_var: Generator, complex_prod_emulation_cmd: List[str]
) -> None:
    """Confirm that complex prod emulation command is parsed correctly."""
    prod_em_creator = TopLevelParser().parse(complex_prod_emulation_cmd)
    assert prod_em_creator.get_commands() == COMPLEX_PROD_COMMANDS_TO_RUN
