"""Models necessary for parsing configuration file."""
from __future__ import annotations

import os
from copy import deepcopy
from typing import (
    Dict,
    NewType,
    Optional,
    Union,
)

from emulation_system.consts import ROOT_DIR
from pydantic import (
    BaseModel,
    ValidationError,
    parse_file_as,
    validator,
)

from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    OT2Model,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    MagneticModuleInputModel,
)

Modules = NewType(
    'Modules',
    Union[
        HeaterShakerModuleInputModel,
        ThermocyclerModuleInputModel,
        TemperatureModuleInputModel,
        MagneticModuleInputModel,
    ]
)

Robots = NewType(
    'Robots',
    Union[OT2Model]
)


class SystemConfigurationModel(BaseModel):
    """Model for overall system configuration specified in a JSON file.

    Represents an entire system to be brought up.
    """

    _ROBOT_IDENTIFIER: str = "robot"
    _MODULES_IDENTIFIER: str = "modules"
    robot: Optional[Dict[str, Robots]]
    modules: Optional[Dict[str, Modules]]

    class Config:
        """Config class used by pydantic."""
        extra = "forbid"

    @validator("robot", pre=True)
    def add_robot_ids(cls, value) -> Dict[str, Union[OT2Model]]:  # noqa: ANN001
        """Parses robot object in JSON file to a RobotModel object."""
        robot_id = list(value.keys())[0]
        value[robot_id]["id"] = robot_id
        return value

    @validator("modules", pre=True)
    def add_module_ids(cls, value) -> Dict[str, Modules]:  # noqa: ANN001
        """Parses all modules in JSON file to a list of ModuleModels."""
        for key, module in value.items():
            module["id"] = key
        return value

    @property
    def containers(self) -> Dict[str, Union[Modules, Robots]]:
        """Return all robots and modules in a single dictionary."""
        robot = deepcopy(self.robot) if self.robot is not None else {}
        # Don't need to deep copy modules because we are going to add to robot var
        modules = self.modules if self.modules is not None else {}
        robot.update(modules)
        return robot


if __name__ == "__main__":
    try:
        location = os.path.join(ROOT_DIR, "emulation_system/resources/new_config.json")
        system_configuration = parse_file_as(SystemConfigurationModel, location)
        for module in system_configuration.containers.values():
            print(
                f"{module.hardware}, "
                f"{module.source_type}, "
                f"{module.emulation_level}: "
                f"{module.get_image_name()}"
            )
    except ValidationError as e:
        print(e)
