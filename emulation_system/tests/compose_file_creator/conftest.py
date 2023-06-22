"""Conftest for compose_file_creator package."""
from typing import Any, Callable, Dict, Literal

import py
import pytest

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    OpentronsRepository,
)
from tests.conftest import SYSTEM_UNIQUE_ID
from tests.testing_config_builder import ConfigDefinition, TestingConfigBuilder
from tests.testing_types import ModuleDeclaration


@pytest.fixture
def opentrons_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("opentrons"))


@pytest.fixture
def opentrons_modules_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons-modules directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("opentrons-modules"))


@pytest.fixture
def ot3_firmware_dir(tmpdir: py.path.local) -> str:
    """Get path to temporary opentrons-modules directory.

    Note that this variable is scoped to the test. So if you call the fixture from
    different places in the test the variable will be the same.
    """
    return str(tmpdir.mkdir("ot3-firmware"))


@pytest.fixture
def make_config(
    opentrons_dir: str,
    opentrons_modules_dir: str,
    ot3_firmware_dir: str,
) -> Callable:
    """Builds configuration object."""

    def _make_config(
        monorepo_source: Literal["latest", "branch", "path"] = "latest",
        ot3_firmware_source: Literal["latest", "branch", "path"] = "latest",
        opentrons_modules_source: Literal["latest", "branch", "path"] = "latest",
        robot: Literal["ot2", "ot3"] | None = None,
        modules: ModuleDeclaration | None = None,
        system_unique_id: str | None = None,
    ) -> Dict[str, Any]:
        config_def = ConfigDefinition(
            opentrons_dir=opentrons_dir,
            opentrons_modules_dir=opentrons_modules_dir,
            ot3_firmware_dir=ot3_firmware_dir,
            monorepo_source=monorepo_source,
            ot3_firmware_source=ot3_firmware_source,
            opentrons_modules_source=opentrons_modules_source,
            robot=robot,
            modules=modules,
            system_unique_id=system_unique_id,
        )
        return TestingConfigBuilder(config_def).make_config()

    return _make_config


@pytest.fixture
def ot2_only(make_config: Callable) -> Dict[str, Any]:
    """Configuration with only an OT-2 robot."""
    return make_config(robot="ot2")


@pytest.fixture
def ot3_only(make_config: Callable) -> Dict[str, Any]:
    """Configuration with only an OT-2 robot."""
    return make_config(robot="ot3")


@pytest.fixture
def ot2_and_modules(make_config: Callable) -> Dict[str, Any]:
    """Configuration with an OT-2 robot and 1 of all modules."""
    return make_config(
        robot="ot2",
        modules={
            "magnetic-module": 1,
            "temperature-module": 1,
            "thermocycler-module": 1,
            "heater-shaker-module": 1,
        },
    )


@pytest.fixture
def ot3_and_modules(make_config: Callable) -> Dict[str, Any]:
    """Configuration with an OT-3 robot and 1 of all modules."""
    return make_config(
        robot="ot3",
        modules={
            "magnetic-module": 1,
            "temperature-module": 1,
            "thermocycler-module": 1,
            "heater-shaker-module": 1,
        },
    )


@pytest.fixture
def modules_only(make_config: Callable) -> Dict[str, Any]:
    """Configuration with modules only."""
    return make_config(
        modules={
            "magnetic-module": 1,
            "temperature-module": 1,
            "thermocycler-module": 1,
            "heater-shaker-module": 1,
        }
    )


@pytest.fixture
def ot2_model(ot2_only: Dict[str, Any]) -> Dict[str, Any]:
    """Model for OT2."""
    return ot2_only["robot"]


@pytest.fixture
def ot3_model(ot3_only: Dict[str, Any]) -> Dict[str, Any]:
    """Model for OT3."""
    return ot3_only["robot"]


@pytest.fixture
def heater_shaker_model(make_config: Callable) -> Dict[str, Any]:
    """Model for Heater-Shaker Module."""
    return make_config(modules={"heater-shaker-module": 1})["modules"][0]


@pytest.fixture
def magdeck_model(make_config: Callable) -> Dict[str, Any]:
    """Model for Magdeck Module."""
    return make_config(modules={"magnetic-module": 1})["modules"][0]


@pytest.fixture
def temperature_model(make_config: Callable) -> Dict[str, Any]:
    """Model for Temperature Module."""
    return make_config(modules={"temperature-module": 1})["modules"][0]


@pytest.fixture
def thermocycler_model(make_config: Callable) -> Dict[str, Any]:
    """Model for Thermocycler Module."""
    return make_config(modules={"thermocycler-module": 1})["modules"][0]


@pytest.fixture
def with_system_unique_id(ot2_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and system-unique-id."""
    ot2_and_modules["system-unique-id"] = SYSTEM_UNIQUE_ID
    return ot2_and_modules


@pytest.fixture
def opentrons_head() -> str:
    """Return head url of opentrons repo from test config file."""
    return OpentronsRepository.OPENTRONS.default_branch


@pytest.fixture
def ot3_firmware_head() -> str:
    """Return head url of ot3-firmware repo from test config file."""
    return OpentronsRepository.OT3_FIRMWARE.default_branch


@pytest.fixture
def ot3_remote_everything_branch(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(
        robot="ot3", monorepo_source="branch", ot3_firmware_source="branch"
    )


@pytest.fixture
def ot3_local_ot3_firmware_remote_monorepo(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and remote robot source."""
    return make_config(
        robot="ot3", monorepo_source="latest", ot3_firmware_source="path"
    )


@pytest.fixture
def ot3_remote_ot3_firmware_local_monorepo(
    make_config: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(
        robot="ot3", monorepo_source="path", ot3_firmware_source="latest"
    )


@pytest.fixture
def ot3_local_everything(
    make_config: Callable,
) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(robot="ot3", monorepo_source="path", ot3_firmware_source="path")


@pytest.fixture
def ot2_remote_everything_branch(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(robot="ot2", monorepo_source="branch")


@pytest.fixture
def ot2_local_source(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(robot="ot2", monorepo_source="path")


@pytest.fixture
def heater_shaker_module_hardware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"heater-shaker-module": 1})


@pytest.fixture
def heater_shaker_module_hardware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return make_config(
        modules={"heater-shaker-module": 1}, opentrons_modules_source="path"
    )


@pytest.fixture
def heater_shaker_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    config = make_config(modules={"heater-shaker-module": 1}, monorepo_source="path")
    config["modules"][0]["emulation-level"] = EmulationLevels.FIRMWARE.value
    return config


@pytest.fixture
def heater_shaker_module_firmware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    config = make_config(modules={"heater-shaker-module": 1})
    config["modules"][0]["emulation-level"] = EmulationLevels.FIRMWARE.value
    return config


@pytest.fixture
def thermocycler_module_hardware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Hardware Thermocycler configuration for local source."""
    return make_config(
        modules={"thermocycler-module": 1}, opentrons_modules_source="path"
    )


@pytest.fixture
def thermocycler_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Firmware Thermocycler configuration for local source."""
    config = make_config(modules={"thermocycler-module": 1}, monorepo_source="path")
    config["modules"][0]["emulation-level"] = EmulationLevels.FIRMWARE.value
    return config


@pytest.fixture
def thermocycler_module_hardware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"thermocycler-module": 1})


@pytest.fixture
def thermocycler_module_firmware_remote(
    thermocycler_module_hardware_remote: Dict[str, Any],
) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    thermocycler_module_hardware_remote["modules"][0][
        "emulation-level"
    ] = EmulationLevels.FIRMWARE.value
    return thermocycler_module_hardware_remote


@pytest.fixture
def temperature_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return make_config(modules={"temperature-module": 1}, monorepo_source="path")


@pytest.fixture
def temperature_module_firmware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"temperature-module": 1})


@pytest.fixture
def magnetic_module_firmware_remote(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for remote source."""
    return make_config(modules={"magnetic-module": 1})


@pytest.fixture
def magnetic_module_firmware_local(make_config: Callable) -> Dict[str, Any]:
    """Get Heater Shaker configuration for local source."""
    return make_config(modules={"magnetic-module": 1}, monorepo_source="path")
