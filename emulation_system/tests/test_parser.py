import pytest
from emulation_system.src.parsers.top_level import top_level_parser
from emulation_system.src.consts import (
    OPENTRONS_MODULES_REPO_DEFAULT_PATH,
    OT3_FIRMWARE_REPO_DEFAULT_PATH,
    OPENTRONS_REPO_DEFAULT_PATH,
    PRODUCTION_MODE_NAME,
    DEVELOPMENT_MODE_NAME
)

BASIC_DEV = "emulator dev".split(" ")
MADE_UP_MODULES_PATH = "/these/are/not/the/modules/you/are/looking/for"
MADE_UP_OPENTRONS_PATH = "/otie/I/am/your/father"
MADE_UP_FIRMWARE_PATH = "/the/force/is/strong/with/this/firmware"
COMPLEX_DEV = (
    "em dev --detached "
    f"--opentrons-modules-repo-path={MADE_UP_MODULES_PATH} "
    f"--opentrons-repo-path={MADE_UP_OPENTRONS_PATH} "
    f"--ot3-firmware-repo-path={MADE_UP_FIRMWARE_PATH}"
).split(" ")

@pytest.fixture
def parser():
    return top_level_parser()


def test_basic_dev_em(parser):
    args = parser.parse_args(BASIC_DEV)
    assert args.command == "emulator"
    assert args.detached is False
    assert args.opentrons_modules_repo_path == OPENTRONS_MODULES_REPO_DEFAULT_PATH
    assert args.opentrons_repo_path == OPENTRONS_REPO_DEFAULT_PATH
    assert args.ot3_firmware_repo_path == OT3_FIRMWARE_REPO_DEFAULT_PATH


def test_complex_dev(parser):
    args = parser.parse_args(COMPLEX_DEV)
    assert args.command == "em"
    assert args.detached is True
    assert args.opentrons_modules_repo_path == MADE_UP_MODULES_PATH
    assert args.opentrons_repo_path == MADE_UP_OPENTRONS_PATH
    assert args.ot3_firmware_repo_path == MADE_UP_FIRMWARE_PATH

