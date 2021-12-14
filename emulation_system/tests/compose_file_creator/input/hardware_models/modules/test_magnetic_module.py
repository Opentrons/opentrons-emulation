import pytest
from pydantic import parse_obj_as
from compose_file_creator.input.hardware_models import MagneticModuleModel
from compose_file_creator.settings import (
    Hardware, EmulationLevel, SourceType
)

ID = "my-magnetic"
HARDWARE = Hardware.MAGNETEIC.value
EMULATION_LEVEL = EmulationLevel.FIRMWARE.value
SOURCE_TYPE = SourceType.LOCAL.value

@pytest.fixture
def magnetic_module_default(tmpdir):
    return {
        "id": ID,
        "hardware": HARDWARE,
        "emulation-level": EMULATION_LEVEL,
        "source-type": SOURCE_TYPE,
        "source-location": str(tmpdir),
        "hardware-specific-attributes": {}
    }


def test_default_magnetic_module(magnetic_module_default):
    mag = parse_obj_as(MagneticModuleModel, magnetic_module_default)
    assert mag.hardware == HARDWARE
    assert mag.id == ID
    assert mag.emulation_level == EMULATION_LEVEL
    assert mag.source_type == SOURCE_TYPE

