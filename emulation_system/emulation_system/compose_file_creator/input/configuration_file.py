"""Models necessary for parsing configuration file."""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Mapping, Optional, TypeGuard, cast

import yaml
from pydantic import Field, parse_file_as, parse_obj_as, root_validator

from emulation_system.consts import DEFAULT_NETWORK_NAME
from opentrons_pydantic_base_model import OpentronsBaseModel

from ...source import MonorepoSource, OpentronsModulesSource, OT3FirmwareSource
from ..config_file_settings import (
    EmulationLevels,
    ExtraMount,
    Hardware,
)
from ..errors import DuplicateHardwareNameError
from ..types.input_types import Containers, Modules, Robots
from ..types.intermediate_types import IntermediateNetworks
from ..utilities.hardware_utils import is_ot3
from ..utilities.yaml_utils import OpentronsEmulationYamlDumper
from .hardware_models import (
    ModuleInputModel,
    OT2InputModel,
    OT3InputModel,
    RobotInputModel,
)


class SystemConfigurationModel(OpentronsBaseModel):
    """Model for overall system configuration specified in a JSON file.

    Represents an entire system to be brought up.
    """

    system_unique_id: Optional[str] = Field(regex=r"^[A-Za-z0-9-]+$", min_length=1)
    robot: Optional[Robots]
    modules: Optional[List[Modules]] = Field(default=[])
    monorepo_source: MonorepoSource = Field(
        default=MonorepoSource(source_location="latest")
    )
    ot3_firmware_source: OT3FirmwareSource = Field(
        default=OT3FirmwareSource(source_location="latest")
    )
    opentrons_modules_source: OpentronsModulesSource = Field(
        default=OpentronsModulesSource(source_location="latest")
    )
    extra_mounts: List[ExtraMount] = Field(default=[])

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

    # Have to have a static method that gets passed the self.modules object to
    # be able to TypeGuard it
    @staticmethod
    def modules_exist(modules: Optional[List[Modules]]) -> TypeGuard[List[Modules]]:
        """Confirm that modules exist in configuration."""
        return (
            modules is not None
            and len(modules) > 0
            and all(
                issubclass(module.__class__, ModuleInputModel) for module in modules
            )
        )

    # Same as above comment but with the robot
    @staticmethod
    def robot_exists(robot: Optional[Robots]) -> TypeGuard[Robots]:
        """Confirm that robot exist in configuration."""
        return robot is not None and issubclass(robot.__class__, RobotInputModel)

    @property
    def requires_can_network(self) -> bool:
        """Whether or not the system requires a CAN network."""
        # Have to cast self.robot because mypy is not picking up that robot_exists
        # is checking for the value of self.robot being None
        return (
            self.robot_exists(self.robot)
            and cast(Robots, self.robot).hardware == Hardware.OT3
        )

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
        if self.robot_exists(self.robot):
            new_dict[self.robot.id] = self.robot  # type: ignore[union-attr, assignment]
        if self.modules_exist:  # type: ignore [truthy-function]
            for module in self.modules:  # type: ignore[union-attr]
                new_dict[module.id] = module
        return new_dict

    def get_by_id(self, container_id: str) -> Containers:
        """Return hardware model by container id."""
        return self.containers[container_id]

    @property
    def is_remote(self) -> bool:
        """Checks if all modules and robots are remote."""
        return all(
            [
                self.monorepo_source.is_remote(),
                self.ot3_firmware_source.is_remote(),
                self.opentrons_modules_source.is_remote(),
            ]
        )

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
    def hardware_level_modules(self) -> List[Modules]:
        """Gets list of all hardware level modules in configuration."""
        user_specified_modules = self.modules
        modules: List[Modules] = []
        if self.modules_exist(user_specified_modules):
            modules = [
                module
                for module in user_specified_modules
                if module.emulation_level is EmulationLevels.HARDWARE
            ]

        return modules

    @property
    def firmware_level_modules(self) -> List[Modules]:
        """Gets list of all firmware level modules in configuration."""
        user_specified_modules = self.modules
        if self.modules_exist(user_specified_modules):
            modules = [
                module
                for module in user_specified_modules
                if module.emulation_level is EmulationLevels.FIRMWARE
            ]
        else:
            modules = []
        return modules

    @property
    def local_ot3_builder_required(self) -> bool:
        """Whether or not a local-ot3-firmware-builder container is required."""
        return is_ot3(self.robot) if self.robot_exists(self.robot) else False

    @property
    def local_opentrons_modules_builder_required(self) -> bool:
        """Whether or not a local-opentrons-modules-builder container is required."""
        needed: bool
        if not self.modules_exist(self.modules):
            needed = False
        else:
            needed = len(self.hardware_level_modules) > 0
        return needed

    @property
    def local_monorepo_builder_required(self) -> bool:
        """Whether or not a local-monorepo-builder container is required."""
        # emulator-proxy cannot be local as of 11/8/2022, including the variable
        # so it is clear that evaluating the source-type of emulator proxy was not missed
        emulator_proxy = False
        modules_are_firmware_level = len(self.firmware_level_modules) > 0

        return any(
            [emulator_proxy, self.robot_exists(self.robot), modules_are_firmware_level]
        )

    @property
    def source_repo_field_aliases(self) -> List[str]:
        """Get list of source field aliases."""
        return [
            field_name.replace("_", "-")
            for field_name in self.__fields__.keys()
            if "source" in field_name
        ]

    # Don't want to worry about having to deal with the signature of the
    # parent method. So just type ignoring it.

    def dict(self, *args, **kwargs) -> Dict[str, Any]:  # noqa: ANN002, ANN003
        """Override default dict logic and add custom logic for source fields."""
        default_dict = super().dict(*args, **kwargs)
        default_dict["monorepo-source"] = self.monorepo_source.source_location
        default_dict["ot3-firmware-source"] = self.ot3_firmware_source.source_location
        default_dict[
            "opentrons-modules-source"
        ] = self.opentrons_modules_source.source_location
        return default_dict

    def to_yaml(self) -> str:
        """Convert to yaml string."""
        return yaml.dump(
            data=self.dict(by_alias=True),
            default_flow_style=False,
            Dumper=OpentronsEmulationYamlDumper,
        )
