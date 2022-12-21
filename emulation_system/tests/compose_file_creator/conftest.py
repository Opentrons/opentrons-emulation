"""Conftest for compose_file_creator package."""
from typing import Any, Callable, Dict, Literal

import py
import pytest

from emulation_system import OpentronsEmulationConfiguration
from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevels,
    Hardware,
    OpentronsRepository,
)

HEATER_SHAKER_MODULE_ID = "shakey-and-warm"
MAGNETIC_MODULE_ID = "fatal-attraction"
TEMPERATURE_MODULE_ID = "temperamental"
THERMOCYCLER_MODULE_ID = "t00-hot-to-handle"
OT2_ID = "brobot"
OT3_ID = "edgar-allen-poebot"
EMULATOR_PROXY_ID = "emulator-proxy"
SMOOTHIE_ID = "smoothie"

SYSTEM_UNIQUE_ID = "testing-1-2-3"
FAKE_COMMIT_ID = "ca82a6dff817ec66f44342007202690a93763949"

ModuleDeclaration = Dict[
    Literal[
        "heater-shaker-module",
        "thermocycler-module",
        "temperature-module",
        "magnetic-module",
    ],
    int,
]


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


def __build_source(
    struct: Dict[str, Any],
    monorepo_source: str,
    ot3_firmware_source: str,
    opentrons_modules_source: str,
    opentrons_dir: str,
    opentrons_modules_dir: str,
    ot3_firmware_dir: str,
) -> None:
    if monorepo_source not in ["latest", "commit_id", "path"]:
        raise ValueError('monorepo_source is not "latest", "commit_id", or "path"')

    if ot3_firmware_source not in ["latest", "commit_id", "path"]:
        raise ValueError('ot3_firmware_source is not "latest", "commit_id", or "path"')

    if opentrons_modules_source not in ["latest", "commit_id", "path"]:
        raise ValueError(
            'opentrons_modules_source is not "latest", "commit_id", or "path"'
        )

    if monorepo_source == "commit_id":
        struct["monorepo-source"] = FAKE_COMMIT_ID
    elif monorepo_source == "path":
        struct["monorepo-source"] = opentrons_dir

    if ot3_firmware_source == "commit_id":
        struct["ot3-firmware-source"] = FAKE_COMMIT_ID
    elif ot3_firmware_source == "path":
        struct["ot3-firmware-source"] = ot3_firmware_dir

    if opentrons_modules_source == "commit_id":
        struct["opentrons-modules-source"] = FAKE_COMMIT_ID
    elif opentrons_modules_source == "path":
        struct["opentrons-modules-source"] = opentrons_modules_dir


def __build_robot(struct: Dict[str, Any], robot: str) -> None:
    if robot is not None and robot not in ["ot2", "ot3"]:
        raise ValueError('robot is not None, "ot2", or "ot3"')

    if robot == "ot2":
        struct["robot"] = {
            "id": OT2_ID,
            "hardware": Hardware.OT2.value,
            "emulation-level": EmulationLevels.FIRMWARE.value,
            "exposed-port": 5000,
            "hardware-specific-attributes": {},
        }
    elif robot == "ot3":
        struct["robot"] = {
            "id": OT3_ID,
            "hardware": Hardware.OT3.value,
            "emulation-level": EmulationLevels.HARDWARE.value,
            "exposed-port": 5000,
            "hardware-specific-attributes": {},
        }


def __build_modules(
    struct: Dict,
    modules_decl: ModuleDeclaration | None,
) -> None:
    if modules_decl is None:
        return
    else:
        struct["modules"] = []

    modules = struct["modules"]
    num_hs = (
        modules_decl["heater-shaker-module"]
        if "heater-shaker-module" in modules_decl
        else 0
    )
    num_temp = (
        modules_decl["temperature-module"]
        if "temperature-module" in modules_decl
        else 0
    )
    num_therm = (
        modules_decl["thermocycler-module"]
        if "thermocycler-module" in modules_decl
        else 0
    )
    num_mag = (
        modules_decl["magnetic-module"] if "magnetic-module" in modules_decl else 0
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


@pytest.fixture
def make_config(
    opentrons_dir: str, opentrons_modules_dir: str, ot3_firmware_dir: str
) -> Callable:
    def _make_config(
        monorepo_source: Literal["latest", "commit_id", "path"] = "latest",
        ot3_firmware_source: Literal["latest", "commit_id", "path"] = "latest",
        opentrons_modules_source: Literal["latest", "commit_id", "path"] = "latest",
        robot: Literal["ot2", "ot3"] | None = None,
        modules: ModuleDeclaration | None = None,
        system_unique_id: str | None = None,
    ) -> Dict[str, Any]:
        default = {
            "monorepo-source": "latest",
            "ot3-firmware-source": "latest",
            "opentrons-modules-source": "latest",
        }

        __build_source(
            default,
            monorepo_source,
            ot3_firmware_source,
            opentrons_modules_source,
            opentrons_dir,
            opentrons_modules_dir,
            ot3_firmware_dir,
        )
        __build_robot(default, robot)
        __build_modules(default, modules)
        if system_unique_id is not None:
            default["system-unique-id"] = system_unique_id

        return default

    return _make_config


@pytest.fixture
def ot2_only(make_config) -> Dict[str, Any]:
    return make_config(robot="ot2")


@pytest.fixture
def ot3_only(make_config) -> Dict[str, Any]:
    return make_config(robot="ot3")


@pytest.fixture
def ot2_and_modules(make_config) -> Dict[str, Any]:
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
def ot3_and_modules(make_config) -> Dict[str, Any]:
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
def modules_only(make_config) -> Dict[str, Any]:
    return make_config(
        modules={
            "magnetic-module": 1,
            "temperature-module": 1,
            "thermocycler-module": 1,
            "heater-shaker-module": 1,
        }
    )


@pytest.fixture
def ot2_model(ot2_only) -> Dict[str, Any]:
    return ot2_only["robot"]


@pytest.fixture
def ot3_model(ot3_only) -> Dict[str, Any]:
    return ot3_only["robot"]


@pytest.fixture
def heater_shaker_model(make_config) -> Dict[str, Any]:
    return make_config(modules={"heater-shaker-module": 1})["modules"][0]


@pytest.fixture
def magdeck_model(make_config) -> Dict[str, Any]:
    return make_config(modules={"magnetic-module": 1})["modules"][0]


@pytest.fixture
def temperature_model(make_config) -> Dict[str, Any]:
    return make_config(modules={"temperature-module": 1})["modules"][0]


@pytest.fixture
def thermocycler_model(make_config) -> Dict[str, Any]:
    return make_config(modules={"thermocycler-module": 1})["modules"][0]


@pytest.fixture
def with_system_unique_id(ot2_and_modules: Dict[str, Any]) -> Dict[str, Any]:
    """Structure of SystemConfigurationModel with robot, modules, and system-unique-id."""
    ot2_and_modules["system-unique-id"] = SYSTEM_UNIQUE_ID
    return ot2_and_modules


@pytest.fixture
def opentrons_head(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return head url of opentrons repo from test config file."""
    return testing_global_em_config.get_repo_head(OpentronsRepository.OPENTRONS)


@pytest.fixture
def ot3_firmware_head(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return head url of ot3-firmware repo from test config file."""
    return testing_global_em_config.get_repo_head(OpentronsRepository.OT3_FIRMWARE)


@pytest.fixture
def opentrons_commit(testing_global_em_config: OpentronsEmulationConfiguration) -> str:
    """Return commit url of opentrons repo from test config file."""
    return testing_global_em_config.get_repo_commit(
        OpentronsRepository.OPENTRONS
    ).replace("{{commit-sha}}", FAKE_COMMIT_ID)


@pytest.fixture
def ot3_firmware_commit(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> str:
    """Return commit url of ot3-firmware repo from test config file."""
    return testing_global_em_config.get_repo_commit(
        OpentronsRepository.OT3_FIRMWARE
    ).replace("{{commit-sha}}", FAKE_COMMIT_ID)


@pytest.fixture
def ot3_remote_everything_commit_id(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(
        robot="ot3", monorepo_source="commit_id", ot3_firmware_source="commit_id"
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
def ot2_remote_everything_commit_id(make_config: Callable) -> Dict[str, Any]:
    """Get OT3 configured for local source and local robot source."""
    return make_config(robot="ot2", monorepo_source="commit_id")


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
