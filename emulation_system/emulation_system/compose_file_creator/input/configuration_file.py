from __future__ import annotations

import json
import os
from typing import List, Union, Optional

from pydantic import BaseModel, ValidationError, parse_obj_as

from emulation_system.compose_file_creator.input.hardware_models import (
    HardwareModel,
    ModuleModel,
    RobotModel,
    HeaterShakerModuleModel,
    ThermocyclerModuleModel,
    TemperatureModuleModel,
    OT2Model

)

from emulation_system.consts import ROOT_DIR


class ContainerDefinitionModel(BaseModel):
    __root__: Union[
        HeaterShakerModuleModel,
        ThermocyclerModuleModel,
        TemperatureModuleModel,
        OT2Model
    ]

    @staticmethod
    def convert_to_hardware_container(
            model: ContainerDefinitionModel
    ) -> HardwareModel:
        """Converts ContainerDefintionModel object to a HardwareModel object"""
        return parse_obj_as(ContainerDefinitionModel, model).__root__


class SystemConfiguration(BaseModel):
    robot: Optional[HardwareModel]
    modules: Optional[List[ModuleModel]]
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
