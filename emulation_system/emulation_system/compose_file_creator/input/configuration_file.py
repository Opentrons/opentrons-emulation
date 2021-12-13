from __future__ import annotations

import json
import os
from typing import List, Union, Optional, Dict
from pydantic import BaseModel, ValidationError, parse_obj_as, validator, \
    root_validator, parse_file_as

from compose_file_creator.input.hardware_models import MagneticModuleModel
from emulation_system.consts import ROOT_DIR
from emulation_system.compose_file_creator.input.hardware_models\
    .modules.module_model import ModuleModel
from emulation_system.compose_file_creator.input.hardware_models\
    .robots.robot_model import RobotModel
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleModel,
    ThermocyclerModuleModel,
    TemperatureModuleModel,
    OT2Model

)


class RobotParser(BaseModel):
    """Class to parse out robots. Makes use of pydantic's ability to parse literals
    The literal is the `hardware` key on all hardware objects"""
    __root__: Union[
        OT2Model
    ]


class ModuleParser(BaseModel):
    """Class to parse out modules Makes use of pydantic's ability to parse literals
    The literal is the `hardware` key on all hardware objects"""
    __root__: Union[
        HeaterShakerModuleModel,
        ThermocyclerModuleModel,
        TemperatureModuleModel,
        MagneticModuleModel
    ]


class SystemConfigurationModel(BaseModel):
    """Model for overall system configuration specified in a JSON file.
    Represents an entire system to be brought up"""
    _ROBOT_IDENTIFIER = "robot"
    _MODULES_IDENTIFIER = "modules"
    robot: Optional[Dict[str, RobotParser]]
    modules: Optional[Dict[str, ModuleParser]]

    class Config:
        extra = "forbid"

    @validator("robot", pre=True)
    def add_robot_ids(cls, value) -> None:
        """Parses robot object in JSON file to a RobotModel object"""
        robot_id = list(value.keys())[0]
        value[robot_id]['id'] = robot_id
        return value

    @validator("modules", pre=True)
    def add_module_ids(cls, value) -> None:
        """Parses all modules in JSON file to a list of ModuleModels"""
        for key, module in value.items():
            module['id'] = key
        return value

    @root_validator
    def remove_root_key(cls, values):
        for k, v in values['robot'].items():
            values['robot'][k] = v.__root__
        for k, v in values['modules'].items():
            values['modules'][k] = v.__root__
        return values


if __name__ == "__main__":
    try:
        location = os.path.join(ROOT_DIR, "emulation_system/resources/new_config.json")
        system_configuration = parse_file_as(SystemConfigurationModel, location)
        print(system_configuration)
    except ValidationError as e:
        print(e)
