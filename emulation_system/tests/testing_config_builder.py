"""Utility class for building opentrons-emulation configuration dictionaries."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Dict, Literal

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
)
from tests.conftest import (
    FAKE_COMMIT_ID,
    HEATER_SHAKER_MODULE_ID,
    MAGNETIC_MODULE_ID,
    OT2_ID,
    OT3_ID,
    TEMPERATURE_MODULE_ID,
    THERMOCYCLER_MODULE_ID,
)
from tests.testing_types import ModuleDeclaration


@dataclass
class ConfigDefinition:
    """Defines all neccesary input data for creating a testing configuration."""

    opentrons_dir: str
    opentrons_modules_dir: str
    ot3_firmware_dir: str
    monorepo_source: Literal["latest", "commit_id", "path"] = "latest"
    ot3_firmware_source: Literal["latest", "commit_id", "path"] = "latest"
    opentrons_modules_source: Literal["latest", "commit_id", "path"] = "latest"
    robot: Literal["ot2", "ot3"] | None = None
    modules: ModuleDeclaration | None = None
    system_unique_id: str | None = None


class TestingConfigBuilder:
    """Building testing configuration."""

    MONOREPO_NAME = "monorepo-source"
    OT3_FIRMWARE_NAME = "ot3-firmware-source"
    OPENTRONS_MODULES_NAME = "opentrons-modules-source"

    DEFAULT_CONFIG: Dict[str, Any] = {
        MONOREPO_NAME: "latest",
        OT3_FIRMWARE_NAME: "latest",
        OPENTRONS_MODULES_NAME: "latest",
    }

    def __init__(self, config_definition: ConfigDefinition) -> None:
        """Instantiate TestingConfigBuilder object."""
        self._con_def = config_definition
        self._generated_config = deepcopy(self.DEFAULT_CONFIG)

    def __check_for_source_errors(self) -> None:
        if self._con_def.monorepo_source not in ["latest", "commit_id", "path"]:
            raise ValueError('monorepo_source is not "latest", "commit_id", or "path"')

        if self._con_def.ot3_firmware_source not in ["latest", "commit_id", "path"]:
            raise ValueError(
                'ot3_firmware_source is not "latest", "commit_id", or "path"'
            )

        if self._con_def.opentrons_modules_source not in [
            "latest",
            "commit_id",
            "path",
        ]:
            raise ValueError(
                'opentrons_modules_source is not "latest", "commit_id", or "path"'
            )

    def __build_source(self) -> None:
        self.__check_for_source_errors()

        if self._con_def.monorepo_source == "commit_id":
            self._generated_config[self.MONOREPO_NAME] = FAKE_COMMIT_ID
        elif self._con_def.monorepo_source == "path":
            self._generated_config[self.MONOREPO_NAME] = self._con_def.opentrons_dir

        if self._con_def.ot3_firmware_source == "commit_id":
            self._generated_config[self.OT3_FIRMWARE_NAME] = FAKE_COMMIT_ID
        elif self._con_def.ot3_firmware_source == "path":
            self._generated_config[
                self.OT3_FIRMWARE_NAME
            ] = self._con_def.ot3_firmware_dir

        if self._con_def.opentrons_modules_source == "commit_id":
            self._generated_config[self.OPENTRONS_MODULES_NAME] = FAKE_COMMIT_ID
        elif self._con_def.opentrons_modules_source == "path":
            self._generated_config[
                self.OPENTRONS_MODULES_NAME
            ] = self._con_def.opentrons_modules_dir

    def __build_robot(self) -> None:
        if self._con_def.robot is None:
            return

        if self._con_def.robot is not None and self._con_def.robot not in [
            "ot2",
            "ot3",
        ]:
            raise ValueError('robot is not None, "ot2", or "ot3"')

        if self._con_def.robot == "ot2":
            self._generated_config["robot"] = {
                "id": OT2_ID,
                "hardware": Hardware.OT2.value,
                "emulation-level": EmulationLevels.FIRMWARE.value,
                "exposed-port": 5000,
                "hardware-specific-attributes": {},
            }
        elif self._con_def.robot == "ot3":
            self._generated_config["robot"] = {
                "id": OT3_ID,
                "hardware": Hardware.OT3.value,
                "emulation-level": EmulationLevels.HARDWARE.value,
                "exposed-port": 5000,
                "hardware-specific-attributes": {},
            }

    def __build_modules(self) -> None:
        if self._con_def.modules is None:
            return
        modules = self._generated_config["modules"] = []
        num_hs = (
            self._con_def.modules["heater-shaker-module"]
            if "heater-shaker-module" in self._con_def.modules
            else 0
        )
        num_temp = (
            self._con_def.modules["temperature-module"]
            if "temperature-module" in self._con_def.modules
            else 0
        )
        num_therm = (
            self._con_def.modules["thermocycler-module"]
            if "thermocycler-module" in self._con_def.modules
            else 0
        )
        num_mag = (
            self._con_def.modules["magnetic-module"]
            if "magnetic-module" in self._con_def.modules
            else 0
        )

        if num_hs > 0:
            hs_list = [
                {
                    "id": f"{HEATER_SHAKER_MODULE_ID}-{i}",
                    "hardware": Hardware.HEATER_SHAKER_MODULE.value,
                    "emulation-level": EmulationLevels.HARDWARE.value,
                    "hardware-specific-attributes": {},
                }
                for i in range(1, num_hs + 1)
            ]
            modules.extend(hs_list)

        if num_temp > 0:
            temp_list = [
                {
                    "id": f"{TEMPERATURE_MODULE_ID}-{i}",
                    "hardware": Hardware.TEMPERATURE_MODULE.value,
                    "emulation-level": EmulationLevels.FIRMWARE.value,
                    "hardware-specific-attributes": {},
                }
                for i in range(1, num_temp + 1)
            ]
            modules.extend(temp_list)

        if num_therm > 0:
            therm_list = [
                {
                    "id": f"{THERMOCYCLER_MODULE_ID}-{i}",
                    "hardware": Hardware.THERMOCYCLER_MODULE.value,
                    "emulation-level": EmulationLevels.HARDWARE.value,
                    "hardware-specific-attributes": {},
                }
                for i in range(1, num_therm + 1)
            ]
            modules.extend(therm_list)

        if num_mag > 0:
            mag_list = [
                {
                    "id": f"{MAGNETIC_MODULE_ID}-{i}",
                    "hardware": Hardware.MAGNETIC_MODULE.value,
                    "emulation-level": EmulationLevels.FIRMWARE.value,
                    "hardware-specific-attributes": {},
                }
                for i in range(1, num_mag + 1)
            ]
            modules.extend(mag_list)

    def __set_system_unique_id(self) -> None:
        user_defined_system_unique_id = self._con_def.system_unique_id
        if user_defined_system_unique_id is not None:
            self._generated_config["system-unique-id"] = user_defined_system_unique_id

    def make_config(self) -> Dict[str, Any]:
        """Build the config."""
        self.__build_source()
        self.__build_robot()
        self.__build_modules()
        self.__set_system_unique_id()

        return self._generated_config
