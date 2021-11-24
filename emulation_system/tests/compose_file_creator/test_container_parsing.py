import pytest
from pydantic import ValidationError
from compose_file_creator.input.models.container import ContainerModel
from compose_file_creator.input.settings import (
    Hardware, HeaterShakerModes, EmulationLevel, SourceType
)

NAME = "Heater Shaker Test"
HARDWARE = "Heater Shaker Module"
EMULATION_LEVEL = "firmware"
SOURCE_TYPE = "remote"
SOURCE_LOCATION = "latest"

MINIMAL_HEATER_SHAKER = {
        "name": NAME,
        "attributes": {
            "hardware": HARDWARE,
            "emulation-level": EMULATION_LEVEL,
            "source-type": SOURCE_TYPE,
            "source-location": SOURCE_LOCATION,
        }
    }
HEATER_SHAKER_WITH_MODE = {
        "name": NAME,
        "attributes": {
            "hardware": HARDWARE,
            "emulation-level": EMULATION_LEVEL,
            "source-type": SOURCE_TYPE,
            "source-location": SOURCE_LOCATION,
            "mode": "stdin"
        }
    }


HEATER_SHAKER_WITH_BAD_MODE = {
        "name": NAME,
        "attributes": {
            "hardware": HARDWARE,
            "emulation-level": EMULATION_LEVEL,
            "source-type": SOURCE_TYPE,
            "source-location": SOURCE_LOCATION,
            "mode": "invalid mode"
        }
    }


VALID_HEATER_SHAKER_CONFIGS = [
    MINIMAL_HEATER_SHAKER,
    HEATER_SHAKER_WITH_MODE
]

INVALID_HEATER_SHAKER_CONFIGS = [
    HEATER_SHAKER_WITH_BAD_MODE
]


def test_minimal_heater_shaker():
    container = ContainerModel.from_dict(MINIMAL_HEATER_SHAKER)
    assert container.name == NAME
    assert container.attributes.hardware == HARDWARE
    assert container.attributes.emulation_level == EMULATION_LEVEL
    assert container.attributes.source_type == SOURCE_TYPE
    assert container.attributes.source_location == SOURCE_LOCATION
    assert container.attributes.mode == "socket"


def test_heater_shaker_with_mode():
    container = ContainerModel.from_dict(HEATER_SHAKER_WITH_MODE)
    assert container.name == NAME
    assert container.attributes.hardware == HARDWARE
    assert container.attributes.emulation_level == EMULATION_LEVEL
    assert container.attributes.source_type == SOURCE_TYPE
    assert container.attributes.source_location == SOURCE_LOCATION
    assert container.attributes.mode == "stdin"


def test_heater_shaker_with_bad_mode():
    with pytest.raises(ValidationError):
        ContainerModel.from_dict(HEATER_SHAKER_WITH_BAD_MODE)
