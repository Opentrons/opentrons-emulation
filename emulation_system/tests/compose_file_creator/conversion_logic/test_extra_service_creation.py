"""Tests for the creation of services not directly defined in input file.

These will be emulation-proxy, smoothie, and ot3 firmware services
Tests for checking env variables, such as pipettes for smoothie, are in
test_environment_variables.py
"""

from typing import Any, Dict

import pytest
from pytest_lazyfixture import lazy_fixture  # type: ignore[import]

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from emulation_system.compose_file_creator.settings.config_file_settings import (
    OT3Hardware,
    SourceType,
)
from emulation_system.compose_file_creator.settings.images import (
    OT3GantryXImages,
    OT3GantryYImages,
    OT3HeadImages,
    OT3PipettesImages,
    SmoothieImages,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)
from tests.compose_file_creator.conftest import EMULATOR_PROXY_ID, SMOOTHIE_ID
from tests.compose_file_creator.conversion_logic.conftest import partial_string_in_mount


@pytest.fixture
def ot2_only_with_remote_source_type(ot2_default: Dict[str, Any]) -> Dict[str, Any]:
    """An OT2 with remote source-type."""
    ot2_default["source-type"] = SourceType.REMOTE
    ot2_default["source-location"] = "latest"
    return {"robot": ot2_default}


@pytest.mark.parametrize(
    "config",
    [
        lazy_fixture(name)
        for name in [
            "ot2_and_modules",
            "modules_only",
            "ot3_and_modules",
            "ot2_only",
            "ot3_only",
        ]
    ],
)
def test_emulation_proxy_created(
    config: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Verify emulator proxy is created when there are modules."""
    services = convert_from_obj(config, testing_global_em_config).services
    assert services is not None
    assert EMULATOR_PROXY_ID in set(services.keys())


@pytest.mark.parametrize(
    "config",
    [lazy_fixture(name) for name in ["ot3_only", "modules_only", "ot3_and_modules"]],
)
def test_smoothie_not_created(
    config: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Confirm smoothie is created only when ot2 exists."""
    services = convert_from_obj(config, testing_global_em_config).services
    assert services is not None
    assert SMOOTHIE_ID not in set(services.keys())


@pytest.mark.parametrize(
    "config", [lazy_fixture(name) for name in ["ot2_only", "ot2_and_modules"]]
)
def test_smoothie_created(
    config: Dict[str, Any], testing_global_em_config: OpentronsEmulationConfiguration
) -> None:
    """Confirm smoothie is created only when ot2 exists."""
    services = convert_from_obj(config, testing_global_em_config).services
    assert services is not None
    assert SMOOTHIE_ID in set(services.keys())


def test_smoothie_with_local_source(
    ot2_only: Dict[str, Any],
    opentrons_dir: str,
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm smoothie uses local source when OT2 is set to local and has mounts."""
    services = convert_from_obj(ot2_only, testing_global_em_config).services
    assert services is not None
    smoothie = services[SMOOTHIE_ID]
    assert smoothie.image == f"{SmoothieImages().local_firmware_image_name}:latest"
    smoothie_mounts = smoothie.volumes
    assert smoothie_mounts is not None
    assert len(smoothie_mounts) > 0
    assert f"{opentrons_dir}:/opentrons" in smoothie_mounts


def test_smoothie_with_remote_source(
    ot2_only_with_remote_source_type: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm smoothie uses remote source when OT2 is set to remote and doesn't have mounts."""  # noqa: E501
    services = convert_from_obj(
        ot2_only_with_remote_source_type, testing_global_em_config
    ).services
    assert services is not None
    smoothie = services[SMOOTHIE_ID]
    assert smoothie.image == f"{SmoothieImages().remote_firmware_image_name}:latest"
    assert smoothie.volumes is None


@pytest.mark.parametrize(
    "container_name, expected_image_name",
    [
        [OT3Hardware.PIPETTES.value, OT3PipettesImages().local_hardware_image_name],
        [OT3Hardware.HEAD.value, OT3HeadImages().local_hardware_image_name],
        [OT3Hardware.GANTRY_X.value, OT3GantryXImages().local_hardware_image_name],
        [OT3Hardware.GANTRY_Y.value, OT3GantryYImages().local_hardware_image_name],
    ],
)
def test_local_ot3_services_created(
    container_name: str,
    expected_image_name: str,
    ot3_only: Dict[str, Any],
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> None:
    """Confirm OT3 hardware emulators are added with OT3 is specified."""
    services = convert_from_obj(ot3_only, testing_global_em_config).services
    assert services is not None
    assert container_name in list(services.keys())

    service = services[container_name]
    assert service.image == expected_image_name

    partial_string_in_mount("entrypoint.sh:/entrypoint.sh", service.volumes)
    partial_string_in_mount("ot3-firmware:/ot3-firmware", service.volumes)
