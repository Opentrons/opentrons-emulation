"""Utilities for emulation_system tests."""
import os

import pytest

from emulation_system import github_api_interaction
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


def get_test_conf() -> OpentronsEmulationConfiguration:
    """Returns configuration settings from test config file."""
    return OpentronsEmulationConfiguration.from_file_path(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_configuration.json"
        )
    )


@pytest.fixture
def testing_global_em_config() -> OpentronsEmulationConfiguration:
    """Get test configuration of OpentronsEmulationConfiguration."""
    return get_test_conf()


HEATER_SHAKER_MODULE_ID = "shakey-and-warm"
MAGNETIC_MODULE_ID = "fatal-attraction"
TEMPERATURE_MODULE_ID = "temperamental"
THERMOCYCLER_MODULE_ID = "t00-hot-to-handle"
OT2_ID = "brobot"
OT3_ID = "edgar-allen-poebot"
EMULATOR_PROXY_ID = "emulator-proxy"
SMOOTHIE_ID = "smoothie"
OT3_STATE_MANAGER_ID = "ot3-state-manager"
MONOREPO_BUILDER_ID = "monorepo-builder"
OPENTRONS_MODULES_BUILDER_ID = "opentrons-modules-builder"
OT3_FIRMWARE_BUILDER_ID = "ot3-firmware-builder"
SYSTEM_UNIQUE_ID = "testing-1-2-3"
FAKE_COMMIT_ID = "ca82a6dff817ec66f44342007202690a93763949"


@pytest.fixture(autouse=True)
def patch_github_api_is_up(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch the github api is up method to always return true."""
    print("Not hitting Github")
    monkeypatch.setattr(github_api_interaction, "github_api_is_up", lambda: True)


@pytest.fixture(autouse=True)
def patch_check_if_branch_exists(monkeypatch: pytest.MonkeyPatch) -> None:
    """Patch the github api is up method to always return true."""

    def inner_func(owner: str, repo: str, branch: str) -> bool:
        print("Not hitting Github")
        match repo:
            case OpentronsRepository.OPENTRONS.value | OpentronsRepository.OPENTRONS_MODULES.value:
                return branch == "edge"
            case OpentronsRepository.OT3_FIRMWARE.value:
                return branch == "main"
            case _:
                raise ValueError(f"Unknown repo {repo}")

    monkeypatch.setattr(github_api_interaction, "check_if_branch_exists", inner_func)
