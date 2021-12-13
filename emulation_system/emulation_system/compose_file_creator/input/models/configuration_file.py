from __future__ import annotations

import json
import os
import re
from typing import List, Union, Optional

from pydantic import BaseModel, ValidationError, Field, parse_obj_as, validator
from typing_extensions import Literal

from emulation_system.compose_file_creator.input.models.hardware_specific_attributes import \
    OT2Attributes
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


class ModuleContainer(HardwareContainer):
    pass


class RobotContainer(HardwareContainer):
    pass


class OT2(RobotContainer):
    hardware: Literal["OT-2"]
    hardware_specific_attributes: OT2Attributes = Field(
        alias="hardware-specific-attributes",
        default=OT2Attributes()
    )


class HeaterShakerModule(ModuleContainer):
    hardware: Literal["heater-shaker"]
    hardware_specific_attributes: HeaterShakerModuleAttributes = Field(
        alias="hardware-specific-attributes",
        default=HeaterShakerModuleAttributes()
    )


class ThermocyclerModule(ModuleContainer):
    hardware: Literal["thermocycler"]
    hardware_specific_attributes: ThermocyclerModuleAttributes = Field(
        alias="hardware-specific-attributes",
        default=ThermocyclerModuleAttributes()
    )


class ContainerDefinitionModel(BaseModel):
    __root__: Union[HeaterShakerModule, ThermocyclerModule, OT2]

    @staticmethod
    def convert_to_hardware_container(
            model: ContainerDefinitionModel
    ) -> HardwareContainer:
        """Converts ContainerDefintionModel object to a HardwareContainer object"""
        return parse_obj_as(ContainerDefinitionModel, model).__root__


class SystemConfiguration(BaseModel):
    robot: Optional[HardwareContainer]
    modules: Optional[List[ModuleContainer]]
    _container_name_list = []

    @classmethod
    def parse_robot(cls, robot):
        robot_id = list(robot.keys())[0]
        robot_content = robot[robot_id]
        robot_content['id'] = robot_id
        return ContainerDefinitionModel.convert_to_hardware_container(robot_content)

    @classmethod
    def parse_modules(cls, modules):
        module_list = []
        for key, module in modules.items():
            module['id'] = key
            module_list.append(
                ContainerDefinitionModel.convert_to_hardware_container(module)
            )
        return module_list

    @classmethod
    def from_file(cls, file_location: str) -> SystemConfiguration:
        content = json.load(open(file_location, 'r'))

        robot = None
        module_list = []

        if 'modules' in content:
            module_list = cls.parse_modules(content['modules'])

        if 'robot' in content:
            robot = cls.parse_robot(content['robot'])


        return SystemConfiguration(
            robot=robot,
            modules=module_list
        )


if __name__ == "__main__":
    try:
        location = os.path.join(ROOT_DIR, "emulation_system/resources/new_config.json")
        system_configuration = SystemConfiguration.from_file(location)
        print(system_configuration)
    except ValidationError as e:
        print(e)
