"""Tests for converting input file to DockerComposeFile."""
from typing import (
    Any,
    Dict,
)

import pytest
from pydantic import parse_obj_as

from emulation_system.compose_file_creator.conversion_layer import ConversionLayer
from emulation_system.compose_file_creator.input.configuration_file import (
    SystemConfigurationModel,
)
from emulation_system.compose_file_creator.output.runtime_compose_file_model import (
    RuntimeComposeFileModel,
)


@pytest.fixture
def version_only() -> Dict[str, str]:
    """Input file with only a compose-file-version specified."""
    return {"compose-file-version": "4.0"}


def to_compose_file(input: Dict[str, Any]) -> RuntimeComposeFileModel:
    """Parses dict to SystemConfigurationModel then runs it through ConversionLayer."""
    return ConversionLayer(parse_obj_as(SystemConfigurationModel, input)).compose_model


def test_version(version_only: Dict[str, str]) -> None:
    """Confirms that version is set correctly on compose file."""
    assert to_compose_file(version_only).version == "4.0"
