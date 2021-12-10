from __future__ import annotations

import json
import os.path
import re
from typing import Dict, List
from pydantic import BaseModel, parse_obj_as, ValidationError, Field, validator
from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.heater_shaker_module import HeaterShakerModuleAttributes
from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.thermocycler_module import ThermocyclerModuleAttributes
from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.temperature_module import TemperatureModuleAttributes
from emulation_system.compose_file_creator.input.models.hardware_specific_attributes.base_type import HardwareSpecificAttributes
from emulation_system.compose_file_creator.input.settings import (
    EmulationLevel,
    SourceType,
    Hardware
)
from emulation_system.consts import ROOT_DIR

CONFIG_FILE_LOCATION = os.path.join(ROOT_DIR, "emulation_system/resources/config.json")

HARDWARE_TO_ATTRIBUTES_MAP = {
    Hardware.THERMOCYCLER_MODULE.value: ThermocyclerModuleAttributes,
    Hardware.HEATER_SHAKER_MODULE.value: HeaterShakerModuleAttributes,
    Hardware.TEMPERATURE_MODULE.value: TemperatureModuleAttributes,
}


class ContainerModel(BaseModel):
    _ID_REGEX_FORMAT = re.compile(r"^[a-zA-Z0-9-_]+$")

    id: str
    hardware: Hardware
    emulation_level: EmulationLevel = Field(alias="emulation-level")
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")
    hardware_specific_attributes: HardwareSpecificAttributes = Field(
        alias="hardware-specific-attributes"
    )

    @validator("hardware_specific_attributes", pre=True)
    def get_hardware_attributes(cls, v, values):
        return HARDWARE_TO_ATTRIBUTES_MAP[values['hardware']](**v)

    @validator("source_location")
    def check_source_location(cls, v, values):
        if values['source_type'] == SourceType.LOCAL:
            assert os.path.isdir(v), f"\"{v}\" is not a valid directory path"
        return v

    @validator("id")
    def check_id_format(cls, v):
        assert cls._ID_REGEX_FORMAT.match(v), (
            f"\"{v}\" does not match required format of only alphanumeric characters, "
            f"dashes and underscores"
        )
        return v

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    @classmethod
    def from_dict(cls, config_dict: Dict[str: str]) -> ContainerModel:
        return parse_obj_as(ContainerModel, config_dict)


if __name__ == "__main__":
    try:
        content = json.load(open(CONFIG_FILE_LOCATION, 'r'))
        hardware_list = parse_obj_as(List[ContainerModel], content['hardware'])
        for item in hardware_list:
            print(item)
    except ValidationError as e:
        print(e)