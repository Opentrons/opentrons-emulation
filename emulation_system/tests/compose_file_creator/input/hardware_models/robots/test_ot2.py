import pytest
from pydantic import parse_obj_as
from compose_file_creator.input.hardware_models import OT2Model
from compose_file_creator.settings import (
    Hardware, EmulationLevel, SourceType
)

ID = "my-ot2"
HARDWARE = Hardware.OT2.value
EMULATION_LEVEL = EmulationLevel.FIRMWARE.value
SOURCE_TYPE = SourceType.LOCAL.value

@pytest.fixture
def ot2_default(tmpdir):
    return {
        "id": ID,
        "hardware": HARDWARE,
        "emulation-level": EMULATION_LEVEL,
        "source-type": SOURCE_TYPE,
        "source-location": str(tmpdir),
        "hardware-specific-attributes": {}
    }


@pytest.fixture
def ot2_with_pipettes(ot2_default):
    ot2_default['hardware-specific-attributes']['left-pipette'] = {}
    ot2_default['hardware-specific-attributes']['left-pipette']['model'] = 'test_1'
    ot2_default['hardware-specific-attributes']['left-pipette']['id'] = 'test_1_id'

    ot2_default['hardware-specific-attributes']['right-pipette'] = {}
    ot2_default['hardware-specific-attributes']['right-pipette']['model'] = 'test_2'
    ot2_default['hardware-specific-attributes']['right-pipette']['id'] = 'test_2_id'
    return ot2_default


def test_default_ot2(ot2_default):
    ot2 = parse_obj_as(OT2Model, ot2_default)
    assert ot2.hardware == HARDWARE
    assert ot2.id == ID
    assert ot2.emulation_level == EMULATION_LEVEL
    assert ot2.source_type == SOURCE_TYPE
    assert ot2.hardware_specific_attributes.left_pipette.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.left_pipette.id == "P20SV202020070101"
    assert ot2.hardware_specific_attributes.right_pipette.model == "p20_single_v2.0"
    assert ot2.hardware_specific_attributes.right_pipette.id == "P20SV202020070101"


def test_ot2_with_custom_pipettes(ot2_with_pipettes):
    ot2 = parse_obj_as(OT2Model, ot2_with_pipettes)
    assert ot2.hardware == HARDWARE
    assert ot2.id == ID
    assert ot2.emulation_level == EMULATION_LEVEL
    assert ot2.source_type == SOURCE_TYPE
    assert ot2.hardware_specific_attributes.left_pipette.model == 'test_1'
    assert ot2.hardware_specific_attributes.left_pipette.id == 'test_1_id'
    assert ot2.hardware_specific_attributes.right_pipette.model == 'test_2'
    assert ot2.hardware_specific_attributes.right_pipette.id == 'test_2_id'

