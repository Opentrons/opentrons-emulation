"""Adds functions to generated compose_file_model."""
from typing import Any, List, Optional

import yaml

from emulation_system.compose_file_creator import Service
from emulation_system.compose_file_creator.container_filters import ContainerFilters

from ..utilities.yaml_utils import OpentronsEmulationYamlDumper

# Have to ignore attr-defined errors from mypy because we are calling type: ignore at
# the top of compose_file_model. This causes mypy to think that ComposeSpecification
# and Service do not exist when they actually do.
from .compose_file_model import ComposeSpecification  # type: ignore[attr-defined]


class RuntimeComposeFileModel(ComposeSpecification):
    """Class to add functionality to generated ComposeSpecification model."""

    is_remote: bool

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Initialize ComposeSpecification."""
        super().__init__(**data)

    def to_yaml(self) -> str:
        """Convert pydantic model to yaml."""
        return yaml.dump(
            self.dict(exclude={"is_remote"}, exclude_none=True),
            default_flow_style=False,
            Dumper=OpentronsEmulationYamlDumper
        )

    @property
    def robot_server(self) -> Optional[Service]:
        """Returns robot server service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.ROBOT_SERVER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def emulator_proxy(self) -> Optional[Service]:
        """Returns emulator proxy service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.EMULATOR_PROXY.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def smoothie_emulator(self) -> Optional[Service]:
        """Returns smoothie emulator service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.SMOOTHIE.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_pipette_emulators(self) -> Optional[List[Service]]:
        """Returns OT3 Pipette service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_PIPETTES.container_filter_name
        )
        return service_list if len(service_list) > 0 else None

    @property
    def ot3_gripper_emulator(self) -> Optional[Service]:
        """Returns OT3 Gripper service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_GRIPPER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_bootloader_emulator(self) -> Optional[Service]:
        """Returns OT3 Pipette service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_BOOTLOADER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_head_emulator(self) -> Optional[Service]:
        """Returns OT3 Head service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_HEAD.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_gantry_x_emulator(self) -> Optional[Service]:
        """Returns OT3 Gantry X service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_GANTRY_X.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_gantry_y_emulator(self) -> Optional[Service]:
        """Returns OT3 Gantry Y service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_GANTRY_Y.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_state_manager(self) -> Optional[Service]:
        """Returns OT3 State Manager service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_STATE_MANAGER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_firmware_builder(self) -> Optional[Service]:
        """Returns local ot3-firmware builder service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_FIRMWARE_BUILDER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def monorepo_builder(self) -> Optional[Service]:
        """Returns local monorepo builder service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.MONOREPO_BUILDER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def opentrons_modules_builder(self) -> Optional[Service]:
        """Returns local ot3-firmware builder service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OPENTRONS_MODULES_BUILDER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def source_builders(self) -> Optional[List[Service]]:
        """Returns all source builders if they exist."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.SOURCE_BUILDERS.container_filter_name
        )
        return service_list if len(service_list) > 0 else None

    @property
    def can_server(self) -> Optional[Service]:
        """Returns CAN server service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.CAN_SERVER.container_filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_emulators(self) -> Optional[List[Service]]:
        """Return list of OT3 service if they exist."""
        emulator_list = [
            prop
            for prop in
            [
                self.ot3_head_emulator,
                self.ot3_gantry_x_emulator,
                self.ot3_gantry_y_emulator,
                self.ot3_gripper_emulator,
                self.ot3_bootloader_emulator
            ]
            if prop is not None
        ]

        if self.ot3_pipette_emulators is not None: 
            emulator_list.extend(self.ot3_pipette_emulators)

        return emulator_list if len(emulator_list) > 0 else None

    @property
    def heater_shaker_module_emulators(self) -> Optional[List[Service]]:
        """Return any Heater-Shaker Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.HEATER_SHAKER_MODULES.container_filter_name
        )

    @property
    def hardware_level_heater_shaker_module_emulators(self) -> Optional[List[Service]]:
        """Return any hardware level emulation heater-shaker modules."""
        return self.load_containers_by_filter(
            ContainerFilters.HARDWARE_HEATER_SHAKER_MODULES.container_filter_name,
        )

    @property
    def firmware_level_heater_shaker_module_emulators(self) -> Optional[List[Service]]:
        """Return any firmware level emulation heater-shaker modules."""
        return self.load_containers_by_filter(
            ContainerFilters.FIRMWARE_HEATER_SHAKER_MODULES.container_filter_name,
        )

    @property
    def thermocycler_module_emulators(self) -> Optional[List[Service]]:
        """Return any Thermocycler Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.THERMOCYCLER_MODULES.container_filter_name
        )

    @property
    def hardware_level_thermocycler_module_emulators(self) -> Optional[List[Service]]:
        """Return any hardware level emulation thermocycler modules."""
        return self.load_containers_by_filter(
            ContainerFilters.HARDWARE_THERMOCYCLER_MODULES.container_filter_name,
        )

    @property
    def firmware_level_thermocycler_module_emulators(self) -> Optional[List[Service]]:
        """Return any firmware level emulation thermocycler modules."""
        return self.load_containers_by_filter(
            ContainerFilters.FIRMWARE_THERMOCYCLER_MODULES.container_filter_name,
        )

    @property
    def magnetic_module_emulators(self) -> Optional[List[Service]]:
        """Return Magnetic Module service if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.MAGNETIC_MODULES.container_filter_name
        )

    @property
    def temperature_module_emulators(self) -> Optional[List[Service]]:
        """Return any Temperature Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.TEMPERATURE_MODULES.container_filter_name
        )

    @property
    def module_emulators(self) -> Optional[List[Service]]:
        """Return any Temperature Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.MODULES.container_filter_name
        )

    @property
    def monorepo_wheel_containers(self) -> Optional[List[Service]]:
        """Returns all containers that utilize the monorepo wheel volume."""
        return self.load_containers_by_filter(
            ContainerFilters.MONOREPO_CONTAINERS.container_filter_name,
        )

    def load_containers_by_filter(
        self,
        container_filter: str,
    ) -> List[Service]:
        """Get a list of services based on filter string."""
        services = self.services
        assert services is not None
        return ContainerFilters.filter_services(container_filter, list(services.values()))
