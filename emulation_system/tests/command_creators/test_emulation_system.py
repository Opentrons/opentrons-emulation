"""Tests for emuluation-system subcommand."""
import io
import json
import pathlib
from unittest.mock import (
    DEFAULT,
    Mock,
    patch,
)

import pytest

from emulation_system.commands.emulation_system_command import (
    EmulationSystemCommand,
    InvalidFileExtensionException,
    InvalidFormatPassedToStdinException,
    STDIN_NAME,
    STDOUT_NAME,
)

EXPECTED_YAML = """
networks:
  derek: {}
services: {}
version: '3.8'
""".strip()


def test_json_stdin(capfd: pytest.CaptureFixture) -> None:
    """Confirm reading JSON from stdin works."""
    mock = Mock(spec=io.TextIOWrapper)
    em_system_command = EmulationSystemCommand(mock, mock)
    with patch.multiple(
        em_system_command, input_path=DEFAULT, output_path=DEFAULT
    ) as multiple_patch:
        multiple_patch["input_path"].name = STDIN_NAME
        multiple_patch["output_path"].name = STDOUT_NAME
        multiple_patch["input_path"].read.return_value = json.dumps(
            {"system-unique-id": "derek"}
        )
        em_system_command.execute()

    assert capfd.readouterr().out.strip() == EXPECTED_YAML


def test_yaml_stdin(capfd: pytest.CaptureFixture) -> None:
    """Confirm reading YAML from stdin works."""
    mock = Mock(spec=io.TextIOWrapper)
    em_system_command = EmulationSystemCommand(mock, mock)
    with patch.multiple(
        em_system_command, input_path=DEFAULT, output_path=DEFAULT
    ) as multiple_patch:
        multiple_patch["input_path"].name = STDIN_NAME
        multiple_patch["output_path"].name = STDOUT_NAME
        multiple_patch["input_path"].read.return_value = 'system-unique-id: "derek"'
        em_system_command.execute()

    assert capfd.readouterr().out.strip() == EXPECTED_YAML


def test_invalid_stdin() -> None:
    """Confirm exception is thrown when read content is not YAML or JSON."""
    mock = Mock(spec=io.TextIOWrapper)
    em_system_command = EmulationSystemCommand(mock, mock)
    with patch.multiple(
        em_system_command, input_path=DEFAULT, output_path=DEFAULT
    ) as multiple_patch:
        multiple_patch["input_path"].name = STDIN_NAME
        multiple_patch["output_path"].name = STDOUT_NAME
        multiple_patch["input_path"].read.return_value = "NOT VALID"

        with pytest.raises(InvalidFormatPassedToStdinException):
            em_system_command.execute()


def test_yaml_file_in(capfd: pytest.CaptureFixture) -> None:
    """Confirm you can read from a .yaml file."""
    mock = Mock(spec=io.TextIOWrapper)
    em_system_command = EmulationSystemCommand(mock, mock)
    with patch.multiple(
        em_system_command, input_path=DEFAULT, output_path=DEFAULT
    ) as multiple_patch:
        multiple_patch["input_path"].name = "/fake/file.yaml"
        multiple_patch["output_path"].name = STDOUT_NAME
        multiple_patch["input_path"].read.return_value = 'system-unique-id: "derek"'
        em_system_command.execute()

    assert capfd.readouterr().out.strip() == EXPECTED_YAML


def test_json_file_in(capfd: pytest.CaptureFixture) -> None:
    """Confirm you can read from a .json file."""
    mock = Mock(spec=io.TextIOWrapper)
    em_system_command = EmulationSystemCommand(mock, mock)
    with patch.multiple(
        em_system_command, input_path=DEFAULT, output_path=DEFAULT
    ) as multiple_patch:
        multiple_patch["input_path"].name = "/fake/file.json"
        multiple_patch["output_path"].name = STDOUT_NAME
        multiple_patch["input_path"].read.return_value = json.dumps(
            {"system-unique-id": "derek"}
        )
        em_system_command.execute()

    assert capfd.readouterr().out.strip() == EXPECTED_YAML


def test_invalid_file_extension() -> None:
    """Confirm exception is thrown if file does not have a .yaml or .json ext."""
    mock = Mock(spec=io.TextIOWrapper)
    em_system_command = EmulationSystemCommand(mock, mock)
    with patch.multiple(
        em_system_command, input_path=DEFAULT, output_path=DEFAULT
    ) as multiple_patch:
        multiple_patch["input_path"].name = "/fake/file.txt"
        multiple_patch["output_path"].name = STDOUT_NAME
        multiple_patch["input_path"].read.return_value = json.dumps(
            {"system-unique-id": "derek"}
        )
        with pytest.raises(InvalidFileExtensionException):
            em_system_command.execute()


def test_file_out(tmp_path: pathlib.Path) -> None:
    """Confirm writing to a file works."""
    d = tmp_path / "dir"
    d.mkdir()
    path = d / "test.yaml"
    mock = Mock(spec=io.TextIOWrapper)
    em_system_command = EmulationSystemCommand(mock, mock)
    with patch.multiple(
        em_system_command, input_path=DEFAULT, output_path=DEFAULT
    ) as multiple_patch:
        multiple_patch["input_path"].name = STDIN_NAME
        multiple_patch["output_path"].name = path
        multiple_patch["input_path"].read.return_value = json.dumps(
            {"system-unique-id": "derek"}
        )
        em_system_command.execute()
    assert "".join(open(path, "r").readlines()).strip() == EXPECTED_YAML
