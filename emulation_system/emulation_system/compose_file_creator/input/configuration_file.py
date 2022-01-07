"""Models necessary for parsing configuration file."""
from __future__ import annotations
from collections import Counter
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
    validator,
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

    compose_file_version: Optional[str] = Field(
        defaut="3.8", alias="compose-file-version"
    )
    robot: Optional[Robots]
    modules: Optional[List[Modules]] = Field(default=[])

    class Config:
        """Config class used by pydantic."""

        extra = "forbid"

    @root_validator(pre=True)
    def validate_names(cls, values) -> Dict[str, Dict[str, Containers]]:  # noqa: ANN001
        """Checks all names in the config file and confirms there are no duplicates."""
        robot_key_exists = "robot" in values and values["robot"] is not None
        modules_key_exists = "modules" in values and values["modules"] is not None

        name_list: List[str] = []

        if (
            # Shouldn't really hit this one, as you would be specifying a
            # system with no modules or robots and that is kinda pointless.
            # But it is still an edge case.
            not robot_key_exists
            and not modules_key_exists
        ) or (
            # Only going to have a single piece of hardware so of course there
            # will not be any duplicates.
            robot_key_exists
            and not modules_key_exists
        ):
            return values

        if modules_key_exists:
            # Don't want to use a set comprehension here because I want to maintain
            # duplicates.
            name_list.extend(module["id"] for module in values["modules"])

        if robot_key_exists:
            name_list.append(values["robot"]["id"])

        duplicates = {
            name
            for name, num_of_instances in Counter(name_list).items()
            if num_of_instances > 1
        }
        if len(duplicates) > 0:
            raise DuplicateHardwareNameError(
                "The following container names are "
                "duplicated in the configuration file: "
                f"{', '.join(duplicates)}"
            )

        return values

    @validator("compose_file_version", pre=True, always=True)
    def set_default_version(cls, v: str) -> str:
        """Sets default version if nothing is specified."""
        return v or "3.8"

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
        # mypy type ignores are added in this method because mypy is not detecting that
        # robot_exists and modules_exists is checking if self.robot or self.modules
        # can be None. So it is throwing linting errors about them being None.
        new_dict: Dict[str, Containers] = {}
        if self.robot_exists:
            new_dict[self.robot.id] = self.robot  # type: ignore[union-attr, assignment]
        if self.modules_exist:
            for module in self.modules:  # type: ignore[union-attr]
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
