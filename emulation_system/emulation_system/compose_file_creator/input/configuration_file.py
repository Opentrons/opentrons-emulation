"""Models necessary for parsing configuration file."""
from __future__ import annotations

from typing import (
    Dict,
    List,
    Mapping,
    Optional,
)

from pydantic import (
    BaseModel,
    Field,
    parse_file_as,
    parse_obj_as,
    root_validator,
)

from emulation_system.compose_file_creator.settings.custom_types import (
    Containers,
    Modules,
    Robots,
)


class DuplicateHardwareNameError(Exception):
    """Exception thrown when there is hardware with duplicate names."""


class SystemConfigurationModel(BaseModel):
    """Model for overall system configuration specified in a JSON file.

    Represents an entire system to be brought up.
    """

    robot: Optional[Robots]
    modules: Optional[List[Modules]] = Field(default=[])

    class Config:
        """Config class used by pydantic."""

        extra = "forbid"

    @root_validator(pre=True)
    def validate_names(cls, values) -> Dict[str, Dict[str, Containers]]:  # noqa: ANN001
        """Checks all names in the config file and confirms there are no duplicates."""
        # Only need to check when there is both a robot and modules defined.
        # This is because if there are duplicates in modules then it will fail by
        # definition of how a dict works (no duplicate keys)
        robot_key_exists = "robot" in values and values["robot"] is not None
        modules_key_exists = "modules" in values and values["modules"] is not None
        if robot_key_exists and modules_key_exists:
            robot_name = values["robot"]["id"]
            module_names = [module["id"] for module in values["modules"]]

            if robot_name in module_names:
                raise DuplicateHardwareNameError(
                    "The following container names are "
                    "duplicated in the configuration file: "
                    f"{robot_name}"
                )

        return values

    @property
    def modules_exist(self) -> bool:
        """Returns True if modules were defined in config file, False if not."""
        return self.modules is not None and len(self.modules) > 0

    @property
    def robot_exists(self) -> bool:
        """Returns True if a robot was defined in config file, False if not."""
        return self.robot is not None and isinstance(self.robot, Robots)

    @property
    def containers(self) -> Mapping[str, Containers]:
        """Return all robots and modules in a single dictionary."""
        new_dict: Dict[str, Containers] = {}
        if self.robot_exists:
            new_dict[self.robot.id] = self.robot
        if self.modules_exist:
            for module in self.modules:
                new_dict[module.id] = module
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
