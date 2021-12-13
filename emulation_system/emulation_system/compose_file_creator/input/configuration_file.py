from __future__ import annotations

import json
import os
from typing import List, Union, Optional

from pydantic import BaseModel, ValidationError, parse_obj_as
from emulation_system.compose_file_creator.input.hardware_models\
    .hardware_model import HardwareModel
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

from emulation_system.consts import ROOT_DIR


class RobotParser(BaseModel):
    __root__: Union[
        OT2Model
    ]

    @staticmethod
    def parse_to_robot(
            model: RobotParser
    ) -> RobotModel:
        """Converts ContainerDefintionModel object to a HardwareModel object"""
        return parse_obj_as(RobotParser, model).__root__


class ModuleParser(BaseModel):
    __root__: Union[
        HeaterShakerModuleModel,
        ThermocyclerModuleModel,
        TemperatureModuleModel,
    ]

    @staticmethod
    def parse_to_module(
            model: ModuleParser
    ) -> ModuleModel:
        """Converts ContainerDefintionModel object to a HardwareModel object"""
        return parse_obj_as(ModuleParser, model).__root__


class SystemConfiguration(BaseModel):
    _ROBOT_IDENTIFIER = "robot"
    _MODULES_IDENTIFIER = "modules"
    robot: Optional[RobotModel]
    modules: Optional[List[ModuleModel]]
    _container_name_list = []

    @classmethod
    def parse_robot(cls, robot):
        robot_id = list(robot.keys())[0]
        robot_content = robot[robot_id]
        robot_content['id'] = robot_id
        return RobotParser.parse_to_robot(robot_content)

    @classmethod
    def parse_modules(cls, modules):
        module_list = []
        for key, module in modules.items():
            module['id'] = key
            module_list.append(
                ModuleParser.parse_to_module(module)
            )
        return module_list

    @classmethod
    def from_file(cls, file_location: str) -> SystemConfiguration:
        content = json.load(open(file_location, 'r'))

        robot = None
        module_list = []

        if cls._MODULES_IDENTIFIER in content:
            module_list = cls.parse_modules(content[cls._MODULES_IDENTIFIER])

        if cls._ROBOT_IDENTIFIER in content:
            robot = cls.parse_robot(content[cls._ROBOT_IDENTIFIER])

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
