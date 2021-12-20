"""Models necessary for parsing configuration file."""
from __future__ import annotations

import os
from typing import (
    Dict,
    Mapping,
)

from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    parse_file_as,
    root_validator,
    validator,
)

from emulation_system.compose_file_creator.settings.custom_types import (
    Containers,
    Modules,
    Robots,
)
from emulation_system.consts import ROOT_DIR


class SystemConfigurationModel(BaseModel):
    """Model for overall system configuration specified in a JSON file.

    Represents an entire system to be brought up.
    """

    _ROBOT_IDENTIFIER: str = "robot"
    _MODULES_IDENTIFIER: str = "modules"
    robot: Dict[str, Robots] = Field(default={})
    modules: Dict[str, Modules] = Field(default={})

    class Config:
        """Config class used by pydantic."""

        extra = "forbid"

    @root_validator
    def validate_names(cls, values) -> Dict[str, Dict[str, Containers]]:  # noqa: ANN001
        """Checks all names in the config file and confirms there are no duplicates."""
        robot_names = set(values['robot'].keys())
        module_names = set(values['modules'].keys())

        name_intersections = robot_names.intersection(module_names)
        assert len(name_intersections) == 0, "The following container names are " \
                                             "duplicated in the configuration file: " \
                                             f"{', '.join(name_intersections)}"

        return values

    @validator("robot", pre=True)
    def add_robot_ids(cls, value) -> Dict[str, Robots]:  # noqa: ANN001
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
    def containers(self) -> Mapping[str, Containers]:
        """Return all robots and modules in a single dictionary."""
        new_dict: Dict[str, Containers] = {}
        new_dict.update(self.robot)
        new_dict.update(self.modules)
        return new_dict


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
