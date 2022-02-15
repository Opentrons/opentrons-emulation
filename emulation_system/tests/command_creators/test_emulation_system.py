"""Tests for emuluation-system subcommand."""
import contextlib
import io
import json
from typing import Any, Dict, Generator
from unittest.mock import DEFAULT, Mock, patch

import pytest
import yaml

from emulation_system.commands.emulation_system_command import (
    STDIN_NAME,
    STDOUT_NAME,
    EmulationSystemCommand,
    InvalidFileExtensionException,
)
from emulation_system.opentrons_emulation_configuration import (
    OpentronsEmulationConfiguration,
)


def convert_yaml(yaml_string: str) -> Dict[str, Any]:
    """Converts and removes context because that is tied to local file system."""
    converted_dict = yaml.safe_load(yaml_string)
    for service in converted_dict["services"].values():
        del service["build"]["context"]

    return converted_dict


EXPECTED_YAML = convert_yaml(
    """
    networks:
      derek: {}
    services:
      derek-emulator-proxy:
        build:
          args:
            OPENTRONS_SOURCE_DOWNLOAD_LOCATION: https://github.com/AnotherOrg/opentrons/archive/refs/heads/edge.zip
          context: /home/derek-maggio/Documents/repos/opentrons-emulation/emulation_system/resources/docker/
          target: emulator-proxy-remote
        container_name: derek-emulator-proxy
        environment:
          OT_EMULATOR_heatershaker_proxy: '{"emulator_port": 10004, "driver_port": 11004}'
          OT_EMULATOR_magnetic_proxy: '{"emulator_port": 10002, "driver_port": 11002}'
          OT_EMULATOR_temperature_proxy: '{"emulator_port": 10001, "driver_port": 11001}'
          OT_EMULATOR_thermocycler_proxy: '{"emulator_port": 10003, "driver_port": 11003}'
        image: emulator-proxy-remote:latest
        networks:
        - derek
        tty: true
    version: '3.8'
    """  # noqa: E501
)

JSON_INPUT = json.dumps({"system-unique-id": "derek"})
YAML_INPUT = 'system-unique-id: "derek"'


@contextlib.contextmanager
def patch_command(
    command: EmulationSystemCommand,
    input_name: str,
    output_name: str,
    input_return_value: str,
) -> Generator:
    """Create paramterized patch of EmulationSystemCommand."""
    with patch.multiple(command, input_path=DEFAULT, output_path=DEFAULT) as mp:
        mp["input_path"].name = input_name
        mp["output_path"].name = output_name
        mp["input_path"].read.return_value = input_return_value
        yield mp


def get_output_string(patch_obj: Mock) -> str:
    """Helper function to get text pathed to output."""
    return patch_obj["output_path"].write.call_args[0][0].strip()


@pytest.fixture
def mocked_em_system(
    testing_global_em_config: OpentronsEmulationConfiguration,
) -> EmulationSystemCommand:
    """Get a mocked EmulationSystemCommand."""
    mock = Mock(spec=io.TextIOWrapper)
    return EmulationSystemCommand(mock, mock, testing_global_em_config)


def test_json_stdin(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm reading JSON from stdin works."""
    with patch_command(mocked_em_system, STDIN_NAME, STDOUT_NAME, JSON_INPUT) as mp:
        mocked_em_system.execute()
    assert convert_yaml(get_output_string(mp)) == EXPECTED_YAML


def test_yaml_stdin(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm reading YAML from stdin works."""
    with patch_command(mocked_em_system, STDIN_NAME, STDOUT_NAME, YAML_INPUT) as mp:
        mocked_em_system.execute()

    assert convert_yaml(get_output_string(mp)) == EXPECTED_YAML


def test_yaml_file_in(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm you can read from a .yaml file."""
    with patch_command(
        mocked_em_system, "/fake/file.yaml", STDOUT_NAME, YAML_INPUT
    ) as mp:
        mocked_em_system.execute()

    assert convert_yaml(get_output_string(mp)) == EXPECTED_YAML


def test_json_file_in(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm you can read from a .json file."""
    with patch_command(
        mocked_em_system, "/fake/file.yaml", STDOUT_NAME, JSON_INPUT
    ) as mp:
        mocked_em_system.execute()

    assert convert_yaml(get_output_string(mp)) == EXPECTED_YAML


def test_invalid_file_extension(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm exception is thrown if file does not have a .yaml or .json ext."""
    with patch_command(mocked_em_system, "/fake/file.txt", STDOUT_NAME, YAML_INPUT):
        with pytest.raises(InvalidFileExtensionException):
            mocked_em_system.execute()


def test_file_out(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm writing to a file works."""
    with patch_command(
        mocked_em_system, STDIN_NAME, "/fake/file.yaml", JSON_INPUT
    ) as mp:
        mocked_em_system.execute()

    assert convert_yaml(get_output_string(mp)) == EXPECTED_YAML
