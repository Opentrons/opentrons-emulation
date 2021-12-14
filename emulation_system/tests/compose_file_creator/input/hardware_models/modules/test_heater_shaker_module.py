import pytest
from pydantic import parse_obj_as
from compose_file_creator.input.hardware_models import HeaterShakerModuleModel
from compose_file_creator.settings import (
    HeaterShakerModes, Hardware, EmulationLevel,  SourceType
)

ID = "my-heater-shaker"
HARDWARE = Hardware.HEATER_SHAKER.value
EMULATION_LEVEL = EmulationLevel.HARDWARE.value
SOURCE_TYPE = SourceType.LOCAL.value

@pytest.fixture
def heater_shaker_default(tmpdir):
    return {
        "id": ID,
        "hardware": HARDWARE,
        "emulation-level": EMULATION_LEVEL,
        "source-type": SOURCE_TYPE,
        "source-location": str(tmpdir)
    }

@pytest.fixture
def heater_shaker_use_stdin(heater_shaker_default):
    heater_shaker_default['hardware_specific_attributes'] = {}
    heater_shaker_default['hardware_specific_attributes']['mode'] = HeaterShakerModes.STDIN
    return heater_shaker_default


def test_default_heater_shaker(heater_shaker_default):
    hs = parse_obj_as(HeaterShakerModuleModel, heater_shaker_default)
    assert hs.hardware == HARDWARE
    assert hs.id == ID
    assert hs.emulation_level == EMULATION_LEVEL
    assert hs.source_type == SOURCE_TYPE
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.SOCKET


def test_heater_shaker_with_stdin(heater_shaker_use_stdin):
    hs = parse_obj_as(HeaterShakerModuleModel, heater_shaker_use_stdin)
    assert hs.hardware == HARDWARE
    assert hs.id == ID
    assert hs.emulation_level == EMULATION_LEVEL
    assert hs.source_type == SOURCE_TYPE
    assert hs.hardware_specific_attributes.mode == HeaterShakerModes.STDIN