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
    parse_obj_as,
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

    robot: Dict[str, Robots] = Field(default={})
    modules: Dict[str, Modules] = Field(default={})

    class Config:
        """Config class used by pydantic."""

        extra = "forbid"

    @root_validator
    def validate_names(cls, values) -> Dict[str, Dict[str, Containers]]:  # noqa: ANN001
        """Checks all names in the config file and confirms there are no duplicates."""
        # Only need to check when there is both a robot and modules defined.
        # This is because if there are duplicates in modules then it will fail by
        # definition of how a dict works (no duplicate keys)
        if "robot" in values and "modules" in values:
            robot_names = set(values["robot"].keys())
            module_names = set(values["modules"].keys())

            name_intersections = robot_names.intersection(module_names)
            assert len(name_intersections) == 0, (
                "The following container names are "
                "duplicated in the configuration file: "
                f"{', '.join(name_intersections)}"
            )

        return values

    @validator("robot", pre=True)
    def there_can_only_be_one(cls, value) -> Dict[str, Robots]:  # noqa: ANN001
        """Confirm that there is only 1 robot defined.

        Was hoping to do this with the maxproperties property in the JSONSchema,
        but it seems that pydantic does not support it so I have to do it with
        a validator.
        """
        assert len(value) == 1, "You can only define 1 robot"
        return value

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
    def modules_exist(self) -> bool:
        """Returns True if modules were defined in config file, False if not."""
        return len(self.modules) > 0

    @property
    def robot_exists(self) -> bool:
        """Returns True if a robot was defined in config file, False if not."""
        return len(self.robot) > 0

    @property
    def containers(self) -> Mapping[str, Containers]:
        """Return all robots and modules in a single dictionary."""
        new_dict: Dict[str, Containers] = {}
        new_dict.update(self.robot)
        new_dict.update(self.modules)
        return new_dict

    def get_by_id(self, container_id: str) -> Containers:
        """Return hardware model by container id."""
        return self.containers[container_id]

    @classmethod
    def from_file(cls, file_path: str) -> SystemConfigurationModel:
        """Parse from file."""
        return parse_file_as(cls, file_path)

    @classmethod
    def from_dict(cls, obj: Dict) -> SystemConfigurationModel:
        """Parse from dict."""
        return parse_obj_as(cls, obj)


if __name__ == "__main__":
    try:
        location = os.path.join(ROOT_DIR, "emulation_system/resources/new_config.json")
        system_configuration = SystemConfigurationModel.from_file(location)

        if system_configuration.modules_exist:
            for module in system_configuration.modules.values():
                print(
                    f"{module.id}, "
                    f"{module.hardware}, "
                    f"{module.source_type}, "
                    f"{module.emulation_level}: "
                )
        if system_configuration.robot_exists:
            for robot in system_configuration.robot.values():
                print(
                    f"{robot.id}, "
                    f"{robot.hardware}, "
                    f"{robot.source_type}, "
                    f"{robot.emulation_level}: "
                )
    except ValidationError as e:
        print(e)
