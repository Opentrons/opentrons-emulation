"""Models necessary for parsing configuration file."""
from __future__ import annotations

import os
from typing import (
    Dict,
    NewType,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    ValidationError,
    parse_file_as,
    validator,
)

from consts import ROOT_DIR
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


if __name__ == "__main__":
    try:
        location = os.path.join(ROOT_DIR, "emulation_system/resources/new_config.json")
        system_configuration = parse_file_as(SystemConfigurationModel, location)
        print(system_configuration)
    except ValidationError as e:
        print(e)
