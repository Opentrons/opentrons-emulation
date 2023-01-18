"""Adds functions to generated compose_file_model."""
from typing import Any, List, Optional

import yaml

from emulation_system.compose_file_creator import BuildItem, Service
from emulation_system.compose_file_creator.container_filters import ContainerFilters

from ..images import FirmwareAndHardwareImages, SingleImage
from ..utilities.yaml_utils import OpentronsEmulationYamlDumper

# Have to ignore attr-defined errors from mypy because we are calling type: ignore at
# the top of compose_file_model. This causes mypy to think that ComposeSpecification
# and Service do not exist when they actually do.
from .compose_file_model import ComposeSpecification  # type: ignore[attr-defined]


class RuntimeComposeFileModel(ComposeSpecification):
    """Class to add functionality to generated ComposeSpecification model."""

    is_remote: bool

    def __init__(self, **data: Any) -> None:
        """Initialize ComposeSpecification."""
        super().__init__(**data)

    def _search_for_services(
        self,
        images_to_search_for: List[FirmwareAndHardwareImages | SingleImage],
        inverse: bool = False,
        only_local: bool = False
    ) -> Optional[List[Service]]:
        service_list = []
        assert self.services is not None

        image_names = []
        for image in images_to_search_for:
            image_names.extend(image.get_image_names())

        for service in self.services.values():
            if (
                    only_local
                    and service.image is not None
                    and "local" not in service.image
            ):
                continue
            service_build = service.build
            assert isinstance(service_build, BuildItem)
            if not inverse:
                if service_build.target in image_names:
                    service_list.append(service)
            else:
                if service_build.target not in image_names:
                    service_list.append(service)

        return service_list if len(service_list) > 0 else None

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
            ContainerFilters.ROBOT_SERVER.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def emulator_proxy(self) -> Optional[Service]:
        """Returns emulator proxy service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.EMULATOR_PROXY.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def smoothie_emulator(self) -> Optional[Service]:
        """Returns smoothie emulator service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.SMOOTHIE.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def heater_shaker_module_emulators(self) -> Optional[List[Service]]:
        """Return any Heater-Shaker Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.HEATER_SHAKER_MODULE.filter_name
        )

    @property
    def ot3_pipette_emulator(self) -> Optional[Service]:
        """Returns OT3 Pipette service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_PIPETTES.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_gripper_emulator(self) -> Optional[Service]:
        """Returns OT3 Gripper service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_GRIPPER.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_bootloader_emulator(self) -> Optional[Service]:
        """Returns OT3 Pipette service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_BOOTLOADER.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_head_emulator(self) -> Optional[Service]:
        """Returns OT3 Head service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_HEAD.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_gantry_x_emulator(self) -> Optional[Service]:
        """Returns OT3 Gantry X service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_GANTRY_X.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_gantry_y_emulator(self) -> Optional[Service]:
        """Returns OT3 Gantry Y service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_GANTRY_Y.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_state_manager(self) -> Optional[Service]:
        """Returns OT3 State Manager service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_STATE_MANAGER.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def ot3_firmware_builder(self) -> Optional[Service]:
        """Returns local ot3-firmware builder service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OT3_FIRMWARE_BUILDER.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def monorepo_builder(self) -> Optional[Service]:
        """Returns local monorepo builder service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.MONOREPO_BUILDER.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def opentrons_modules_builder(self) -> Optional[Service]:
        """Returns local ot3-firmware builder service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.OPENTRONS_MODULES_BUILDER.filter_name
        )
        return service_list[0] if len(service_list) > 0 else None

    @property
    def source_builders(self) -> Optional[List[Service]]:
        """Returns all source builders if they exist."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.SOURCE_BUILDERS.filter_name
        )
        return service_list if len(service_list) > 0 else None

    @property
    def can_server(self) -> Optional[Service]:
        """Returns CAN server service if one exists."""
        service_list = self.load_containers_by_filter(
            ContainerFilters.CAN_SERVER.filter_name
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
                self.ot3_pipette_emulator,
                self.ot3_gantry_x_emulator,
                self.ot3_gantry_y_emulator,
                self.ot3_gripper_emulator,
                self.ot3_bootloader_emulator
            ]
            if prop is not None
        ]
        return emulator_list if len(emulator_list) > 0 else None

    @property
    def thermocycler_module_emulators(self) -> Optional[List[Service]]:
        """Return any Thermocycler Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.THERMOCYCLER_MODULE.filter_name
        )

    @property
    def magnetic_module_emulators(self) -> Optional[List[Service]]:
        """Return Magnetic Module service if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.MAGNETIC_MODULE.filter_name
        )

    @property
    def temperature_module_emulators(self) -> Optional[List[Service]]:
        """Return any Temperature Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.TEMPERATURE_MODULE.filter_name
        )

    @property
    def module_emulators(self) -> Optional[List[Service]]:
        """Return any Temperature Module services if one exists."""
        return self.load_containers_by_filter(
            ContainerFilters.MODULES.filter_name
        )

    def load_containers_by_filter(
        self, container_filter: str, local_only: bool = False
    ) -> List[Service]:
        """Get a list of services based on filter string."""
        inverse = False
        if container_filter.startswith("not-"):
            inverse = True
            container_filter = container_filter.replace("not-", "")

        images_to_load = ContainerFilters.load_by_filter_name(container_filter).images
        containers = self._search_for_services(images_to_load, inverse, local_only)

        return (
            [container for container in containers]
            if containers is not None
            else []
        )
