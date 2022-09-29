"""Utilities for emulation_system tests."""
import os

import pytest

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
