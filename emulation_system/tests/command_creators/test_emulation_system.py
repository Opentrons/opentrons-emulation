"""Tests for emuluation-system subcommand."""
import contextlib
import io
import json
from typing import Generator
from unittest.mock import (
    DEFAULT,
    Mock,
    patch,
)

import pytest

from emulation_system.commands.emulation_system_command import (
    EmulationSystemCommand,
    InvalidFileExtensionException,
    STDIN_NAME,
    STDOUT_NAME,
)

EXPECTED_YAML = """
networks:
  derek: {}
services: {}
version: '3.8'
""".strip()

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
def mocked_em_system() -> EmulationSystemCommand:
    """Get a mocked EmulationSystemCommand."""
    mock = Mock(spec=io.TextIOWrapper)
    return EmulationSystemCommand(mock, mock)


def test_json_stdin(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm reading JSON from stdin works."""
    with patch_command(mocked_em_system, STDIN_NAME, STDOUT_NAME, JSON_INPUT) as mp:
        mocked_em_system.execute()

    assert get_output_string(mp) == EXPECTED_YAML


def test_yaml_stdin(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm reading YAML from stdin works."""
    with patch_command(mocked_em_system, STDIN_NAME, STDOUT_NAME, YAML_INPUT) as mp:
        mocked_em_system.execute()

    assert get_output_string(mp) == EXPECTED_YAML


def test_yaml_file_in(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm you can read from a .yaml file."""
    with patch_command(
        mocked_em_system, "/fake/file.yaml", STDOUT_NAME, YAML_INPUT
    ) as mp:
        mocked_em_system.execute()

    assert get_output_string(mp) == EXPECTED_YAML


def test_json_file_in(mocked_em_system: EmulationSystemCommand) -> None:
    """Confirm you can read from a .json file."""
    with patch_command(
        mocked_em_system, "/fake/file.yaml", STDOUT_NAME, JSON_INPUT
    ) as mp:
        mocked_em_system.execute()

    assert get_output_string(mp) == EXPECTED_YAML


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

    assert get_output_string(mp) == EXPECTED_YAML
