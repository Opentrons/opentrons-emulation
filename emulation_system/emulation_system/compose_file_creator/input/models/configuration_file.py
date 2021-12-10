from __future__ import annotations

import json
import os
import re
from typing import ClassVar, List, Union, Dict

from typing_extensions import Literal

from pydantic import BaseModel, ValidationError, Field, parse_obj_as, validator

from emulation_system.compose_file_creator.input.settings import (
    EmulationLevel,
    SourceType, TemperatureModelSettings, HeaterShakerModes
)
from emulation_system.consts import ROOT_DIR


class HardwareContainer(BaseModel):
    _ID_REGEX_FORMAT = re.compile(r"^[a-zA-Z0-9-_]+$")

    emulation_level: EmulationLevel = Field(alias="emulation-level")
    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")
    id: str

    class Config:
        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    @validator("id")
    def check_id_format(cls, v):
        assert cls._ID_REGEX_FORMAT.match(v), (
            f"\"{v}\" does not match required format of only alphanumeric characters, "
            f"dashes and underscores"
        )
        return v

    @validator("source_location")
    def check_source_location(cls, v, values):
        if values['source_type'] == SourceType.LOCAL:
            assert os.path.isdir(v), f"\"{v}\" is not a valid directory path"
        return v


class ThermocyclerModuleAttributes(BaseModel):
    lid_temperature: TemperatureModelSettings = Field(
        alias="lid-temperature", default=TemperatureModelSettings()
    )
    plate_temperature: TemperatureModelSettings = Field(
        alias="plate-temperature", default=TemperatureModelSettings()
    )


class HeaterShakerModuleAttributes(BaseModel):
    mode: HeaterShakerModes = HeaterShakerModes.SOCKET


class HeaterShakerModule(HardwareContainer):
    kind: Literal["heater-shaker"]
    hardware_specific_attributes: HeaterShakerModuleAttributes = Field(
        alias="hardware-specific-attributes",
        default=HeaterShakerModuleAttributes()
    )


class ThermocyclerModule(HardwareContainer):
    kind: Literal["thermocycler"]
    hardware_specific_attributes: ThermocyclerModuleAttributes = Field(
        alias="hardware-specific-attributes",
        default=ThermocyclerModuleAttributes()
    )


class ContainerDefinitionModel(BaseModel):
    __root__: Union[HeaterShakerModule, ThermocyclerModule]

    @staticmethod
    def convert_to_hardware_container(
            model: ContainerDefinitionModel
    ) -> HardwareContainer:
        """Converts ContainerDefintionModel object to a HardwareContainer object"""
        return parse_obj_as(ContainerDefinitionModel, model).__root__

    @classmethod
    def from_config_file(cls, file_location: str) -> List[HardwareContainer]:
        content = json.load(open(file_location, 'r'))
        module_list = []
        for key, module in content['modules'].items():
            module['id'] = key
            module_list.append(cls.convert_to_hardware_container(module))

        return module_list


if __name__ == "__main__":
    try:
        location = os.path.join(ROOT_DIR, "emulation_system/resources/new_config.json")
        hardware_list = ContainerDefinitionModel.from_config_file(location)
        for item in hardware_list:
            print(item)
    except ValidationError as e:
        print(e)
