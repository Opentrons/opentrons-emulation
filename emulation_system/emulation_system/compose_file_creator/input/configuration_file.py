"""Models necessary for parsing configuration file."""
from __future__ import annotations

from collections import Counter
from typing import Dict, List, Mapping, Optional, cast

from pydantic import BaseModel, Field, parse_file_as, parse_obj_as, root_validator

from emulation_system.consts import DEFAULT_NETWORK_NAME

from ..config_file_settings import EmulationLevels, Hardware, SourceType
from ..errors import DuplicateHardwareNameError
from ..types.input_types import Containers, Modules, Robots
from ..types.intermediate_types import IntermediateNetworks
from ..utilities.hardware_utils import is_ot2, is_ot3
from .hardware_models import OT2InputModel, OT3InputModel


class SystemConfigurationModel(BaseModel):
    """Model for overall system configuration specified in a JSON file.

    Represents an entire system to be brought up.
    """

    system_unique_id: Optional[str] = Field(
        alias="system-unique-id", regex=r"^[A-Za-z0-9-]+$", min_length=1
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
            raise DuplicateHardwareNameError(duplicates)

        return values

    @property
    def modules_exist(self) -> bool:
        """Returns True if modules were defined in config file, False if not."""
        return self.modules is not None and len(self.modules) > 0

    @property
    def robot_exists(self) -> bool:
        """Returns True if a robot was defined in config file, False if not."""
        return self.robot is not None

    @property
    def requires_can_network(self) -> bool:
        """Whether or not the system requires a CAN network."""
        # Have to cast self.robot because mypy is not picking up that robot_exists
        # is checking for the value of self.robot being None
        return self.robot_exists and cast(Robots, self.robot).hardware == Hardware.OT3

    @property
    def can_network_name(self) -> str:
        """Returns name of CAN network."""
        return (
            f"{self.system_unique_id}-can-network"
            if self.system_unique_id is not None
            else "can-network"
        )

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

    @property
    def is_remote(self) -> bool:
        """Checks if all modules and robots are remote."""
        robot_is_remote = self.robot.is_remote if self.robot is not None else True
        modules_are_remote = (
            all(module.is_remote for module in self.modules)
            if self.modules is not None and len(self.modules) > 0
            else True
        )

        return robot_is_remote and modules_are_remote

    @property
    def required_networks(self) -> IntermediateNetworks:
        """Get required networks to create for system."""
        local_network_name = (
            DEFAULT_NETWORK_NAME
            if self.system_unique_id is None
            else f"{self.system_unique_id}-{DEFAULT_NETWORK_NAME}"
        )

        required_networks = [cast(str, local_network_name)]
        if self.requires_can_network:
            required_networks.append(self.can_network_name)

        return IntermediateNetworks(required_networks)

    @property
    def has_ot2(self) -> bool:
        """Whether, robot is an OT-2."""
        return self.robot is not None and isinstance(self.robot, OT2InputModel)

    @property
    def has_ot3(self) -> bool:
        """Whether, robot is an OT-3."""
        return self.robot is not None and isinstance(self.robot, OT3InputModel)

    @classmethod
    def from_file(cls, file_path: str) -> SystemConfigurationModel:
        """Parse from file."""
        return parse_file_as(cls, file_path)

    @classmethod
    def from_dict(cls, obj: Dict) -> SystemConfigurationModel:
        """Parse from dict."""
        return parse_obj_as(cls, obj)

    @property
    def local_ot3_builder_required(self) -> bool:
        """Whether or not a local-ot3-firmware-builder container is required."""
        req: bool
        if self.robot is None:
            req = False
        else:
            req = is_ot3(self.robot) and self.robot.source_type == SourceType.LOCAL
        return req

    @property
    def local_opentrons_modules_builder_required(self) -> bool:
        """Whether or not a local-opentrons-modules-builder container is required."""
        if self.modules is None:
            return False
        return any(
            [
                module.emulation_level == EmulationLevels.HARDWARE
                and module.source_type == SourceType.LOCAL
                for module in self.modules
            ]
        )

    @property
    def local_monorepo_builder_required(self) -> bool:
        """Whether or not a local-monorepo-builder container is required."""
        # emulator-proxy cannot be local as of 11/8/2022, including the variable
        # so it is clear that evaluating the source-type of emulator proxy was not missed
        local_emulator_proxy = False
        local_can_server = (
            self.robot is not None
            and is_ot3(self.robot)
            and self.robot.can_server_source_type == SourceType.LOCAL
        )
        local_opentrons_hardware = (
            self.robot is not None
            and is_ot3(self.robot)
            and self.robot.opentrons_hardware_source_type == SourceType.LOCAL
        )
        local_smoothie = (
            self.robot is not None
            and is_ot2(self.robot)
            and self.robot.source_type == SourceType.LOCAL
        )
        local_modules = self.modules is not None and any(
            (
                module.emulation_level == EmulationLevels.FIRMWARE
                and module.source_type == SourceType.LOCAL
            )
            for module in self.modules
        )
        local_robot_server = (
            self.robot is not None
            and self.robot.robot_server_source_type == SourceType.LOCAL
        )

        return any(
            [
                local_emulator_proxy,
                local_can_server,
                local_opentrons_hardware,
                local_smoothie,
                local_modules,
                local_robot_server,
            ]
        )
