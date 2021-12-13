from __future__ import annotations

import json
import os
from typing import List, Union, Optional
from pydantic import BaseModel, ValidationError, parse_obj_as
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

    @staticmethod
    def parse_to_robot(model: RobotParser) -> RobotModel:
        """Parses passed model to one of the classes defined in the above __root__
        attribute"""
        return parse_obj_as(RobotParser, model).__root__


class ModuleParser(BaseModel):
    """Class to parse out modules Makes use of pydantic's ability to parse literals
    The literal is the `hardware` key on all hardware objects"""
    __root__: Union[
        HeaterShakerModuleModel,
        ThermocyclerModuleModel,
        TemperatureModuleModel,
    ]

    @staticmethod
    def parse_to_module(model: ModuleParser) -> ModuleModel:
        """Parses passed model to one of the classes defined in the above __root__
        attribute"""
        return parse_obj_as(ModuleParser, model).__root__


class SystemConfigurationModel(BaseModel):
    """Model for overall system configuration specified in a JSON file.
    Represents an entire system to be brought up"""
    _ROBOT_IDENTIFIER = "robot"
    _MODULES_IDENTIFIER = "modules"
    robot: Optional[RobotModel]
    modules: Optional[List[ModuleModel]]
    _container_name_list = []

    @classmethod
    def parse_robot(cls, robot) -> RobotModel:
        """Parses robot object in JSON file to a RobotModel object"""
        robot_id = list(robot.keys())[0]
        robot_content = robot[robot_id]
        robot_content['id'] = robot_id
        return RobotParser.parse_to_robot(robot_content)

    @classmethod
    def parse_modules(cls, modules) -> List[ModuleModel]:
        """Parses all modules in JSON file to a list of ModuleModels"""
        module_list = []
        for key, module in modules.items():
            module['id'] = key
            module_list.append(
                ModuleParser.parse_to_module(module)
            )
        return module_list

    @classmethod
    def from_file(cls, file_location: str) -> SystemConfigurationModel:
        """Parses JSON file into a SystemConfigurationModel"""
        content = json.load(open(file_location, 'r'))

        robot = None
        module_list = []

        if cls._MODULES_IDENTIFIER in content:
            module_list = cls.parse_modules(content[cls._MODULES_IDENTIFIER])

        if cls._ROBOT_IDENTIFIER in content:
            robot = cls.parse_robot(content[cls._ROBOT_IDENTIFIER])

        return SystemConfigurationModel(
            robot=robot,
            modules=module_list
        )


if __name__ == "__main__":
    try:
        location = os.path.join(ROOT_DIR, "emulation_system/resources/new_config.json")
        system_configuration = SystemConfigurationModel.from_file(location)
        print(system_configuration)
    except ValidationError as e:
        print(e)
