"""Adds functions to generated compose_file_model."""
from typing import (
    Any,
    List,
    Optional,
    Type,
)

import yaml

# Have to ignore attr-defined errors from mypy because we are calling type: ignore at
# the top of compose_file_model. This causes mypy to think that ComposeSpecification
# and Service do not exist when they actually do.
from emulation_system.compose_file_creator.output.compose_file_model import (  # type: ignore[attr-defined] # noqa: E501
    ComposeSpecification,
    Service,
)
from emulation_system.compose_file_creator.settings.images import (
    EmulatorProxyImages,
    HeaterShakerModuleImages,
    Images,
    MagneticModuleImages,
    OT3GantryXImages,
    OT3GantryYImages,
    OT3HeadImages,
    OT3PipettesImages,
    RobotServerImages,
    SmoothieImages,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)


def represent_none(self, _):  # noqa: ANN001 ANN201
    """Override how yaml is formatted and instead of putting null, leave it blank."""
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


class RuntimeComposeFileModel(ComposeSpecification):
    """Class to add functionality to generated ComposeSpecification model."""

    def __init__(self, **data: Any) -> None:
        """Initialize ComposeSpecification."""
        super().__init__(**data)

    def _search_for_services(
        self, class_to_search_for: Type[Images], service_type_name: str
    ) -> Optional[List[Service]]:
        service_list = [
            service
            for service in self.services.values()
            if service.build.target in class_to_search_for().get_image_names()
        ]
        return service_list if len(service_list) > 0 else None

    def to_yaml(self) -> str:
        """Convert pydantic model to yaml."""
        return yaml.dump(self.dict(exclude_none=True), default_flow_style=False)

    @property
    def robot_server(self) -> Optional[Service]:
        """Returns robot server service if one exists."""
        service_list = self._search_for_services(RobotServerImages, "Robot Server")
        if service_list is not None:
            return service_list[0]

    @property
    def emulator_proxy(self) -> Optional[Service]:
        """Returns emulator proxy service if one exists."""
        service_list = self._search_for_services(EmulatorProxyImages, "Emulator Proxy")
        if service_list is not None:
            return service_list[0]

    @property
    def smoothie_emulator(self) -> Optional[Service]:
        """Returns smoothie emulator service if one exists."""
        service_list = self._search_for_services(SmoothieImages, "Smoothie")
        if service_list is not None:
            return service_list[0]

    @property
    def heater_shaker_module_emulators(self) -> Optional[List[Service]]:
        """Return any Heater-Shaker Module services if one exists."""
        return self._search_for_services(
            HeaterShakerModuleImages, "Heater-Shaker Module"
        )

    @property
    def ot3_pipette_emulator(self) -> Optional[Service]:
        """Returns OT3 Pipette service if one exists."""
        service_list = self._search_for_services(OT3PipettesImages, "OT3 Pipette")
        if service_list is not None:
            return service_list[0]

    @property
    def ot3_head_emulator(self) -> Optional[Service]:
        """Returns OT3 Head service if one exists."""
        service_list = self._search_for_services(OT3HeadImages, "OT3 Head")
        if service_list is not None:
            return service_list[0]

    @property
    def ot3_gantry_x_emulator(self) -> Optional[Service]:
        """Returns OT3 Gantry X service if one exists."""
        service_list = self._search_for_services(OT3GantryXImages, "OT3 Gantry X")
        if service_list is not None:
            return service_list[0]

    @property
    def ot3_gantry_y_emulator(self) -> Optional[Service]:
        """Returns OT3 Gantry Y service if one exists."""
        service_list = self._search_for_services(OT3GantryYImages, "OT3 Gantry Y")
        if service_list is not None:
            return service_list[0]

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
                self.ot3_gantry_y_emulator
            ]
            if prop is not None
        ]
        return emulator_list if len(emulator_list) > 0 else None

    @property
    def thermocycler_module_emulators(self) -> Optional[List[Service]]:
        """Return any Thermocycler Module services if one exists."""
        return self._search_for_services(
            ThermocyclerModuleImages, "Thermocycler Module"
        )

    @property
    def magnetic_module_emulators(self) -> Optional[List[Service]]:
        """Return Magnetic Module service if one exists."""
        return self._search_for_services(MagneticModuleImages, "Magnetic Module")

    @property
    def temperature_module_emulators(self) -> Optional[List[Service]]:
        """Return any Temperature Module services if one exists."""
        return self._search_for_services(TemperatureModuleImages, "Temperature Module")
