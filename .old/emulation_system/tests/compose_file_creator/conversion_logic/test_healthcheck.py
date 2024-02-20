"""Test docker-compose healthcheck fields for all emulators."""

from typing import Any, Dict

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.images import (
    HeaterShakerModuleImages,
    MagneticModuleImages,
    TemperatureModuleImages,
    ThermocyclerModuleImages,
)
from emulation_system.compose_file_creator.input.hardware_models import (
    HeaterShakerModuleInputModel,
    MagneticModuleInputModel,
    TemperatureModuleInputModel,
    ThermocyclerModuleInputModel,
)

MODULE_IMAGE_NAMES = (
    HeaterShakerModuleImages().get_image_names(True, True)
    + MagneticModuleImages().get_image_names(True, True)
    + TemperatureModuleImages().get_image_names(True, True)
    + ThermocyclerModuleImages().get_image_names(True, True)
)


def test_ot3_services_heathcheck(
    ot3_only: Dict[str, Any],
) -> None:
    """Confirm all ot3 firmware service and can-server healthchecks are correct."""
    services = convert_from_obj(ot3_only, False).services
    assert services is not None
    services_to_check = [
        service
        for service in services.values()
        if service.image is not None
        and "state-manager" not in service.image
        and "ot3-firmware-builder" not in service.image
        and ("ot3" in service.image or "can-server" in service.image)
    ]
    assert len(services_to_check) == 8
    for service in services_to_check:
        healthcheck = service.healthcheck
        assert healthcheck is None


def test_emulator_proxy_heathcheck(
    ot3_only: Dict[str, Any],
) -> None:
    """Confirm emulator proxy healthcheck is configured correctly."""
    services = convert_from_obj(ot3_only, False).services
    assert services is not None
    services_to_check = [
        service
        for service in services.values()
        if service.image is not None and "emulator-proxy" in service.image
    ]
    assert len(services_to_check) == 1
    for service in services_to_check:
        healthcheck = service.healthcheck
        assert healthcheck is None


def test_local_ot3_firmware_builder_heathcheck(
    ot3_only: Dict[str, Any],
) -> None:
    """Confirm emulator proxy healthcheck is configured correctly."""
    services = convert_from_obj(ot3_only, False).services
    assert services is not None
    services_to_check = [
        service
        for service in services.values()
        if service.image is not None and "ot3-firmware-builder" in service.image
    ]
    assert len(services_to_check) == 1
    for service in services_to_check:
        healthcheck = service.healthcheck
        assert healthcheck is not None
        assert healthcheck.interval == "10s"
        assert healthcheck.timeout == "10s"
        assert healthcheck.test == "(cd /ot3-firmware) && (cd /opentrons)"
        assert healthcheck.start_period is None
        assert healthcheck.disable is None


def test_smoothie_heathcheck(
    ot2_only: Dict[str, Any],
) -> None:
    """Confirm smoothie healthcheck is configured correctly."""
    services = convert_from_obj(ot2_only, False).services
    assert services is not None
    services_to_check = [
        service
        for service in services.values()
        if service.image is not None and "smoothie" in service.image
    ]
    assert len(services_to_check) == 1
    for service in services_to_check:
        healthcheck = service.healthcheck
        assert healthcheck is None


@pytest.mark.parametrize("config", [lazy_fixture("ot2_only"), lazy_fixture("ot3_only")])
def test_robot_server_healthcheck(
    config: Dict[str, Any],
) -> None:
    """Confirm healthcheck for robot-server on both OT-2 and OT-3 is correct."""
    services = convert_from_obj(config, False).services
    assert services is not None
    services_to_check = [
        service
        for service in services.values()
        if service.image is not None and "robot-server" in service.image
    ]
    assert len(services_to_check) == 1
    for service in services_to_check:
        healthcheck = service.healthcheck
        assert healthcheck is None


def __lookup_module_port(module_image: str) -> int:
    module_image = module_image.replace(":latest", "")
    if module_image in HeaterShakerModuleImages().get_image_names():
        port = HeaterShakerModuleInputModel.proxy_info.emulator_port
    elif module_image in MagneticModuleImages().get_image_names():
        port = MagneticModuleInputModel.proxy_info.emulator_port
    elif module_image in ThermocyclerModuleImages().get_image_names():
        port = ThermocyclerModuleInputModel.proxy_info.emulator_port
    elif module_image in TemperatureModuleImages().get_image_names():
        port = TemperatureModuleInputModel.proxy_info.emulator_port
    else:
        raise Exception("You passed a bad module image")
    return port


def test_modules_healthcheck(
    ot2_and_modules: Dict[str, Any],
) -> None:
    """Confirm all 4 module's healthcheck is correct."""
    services = convert_from_obj(ot2_and_modules, False).services
    assert services is not None

    services_to_check = [
        service
        for service in services.values()
        if service.image is not None
        and service.image.replace(":latest", "") in MODULE_IMAGE_NAMES
    ]
    assert len(services_to_check) == 4

    for service in services_to_check:
        assert service.image is not None
        healthcheck = service.healthcheck
        assert healthcheck is None
