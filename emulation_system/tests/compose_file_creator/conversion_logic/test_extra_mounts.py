"""Tests related to extra-mounts on services"""
from pathlib import Path
from typing import Any, Dict, List

import pytest

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from tests.validation_helper_functions import mount_string_is


@pytest.fixture
def extra_file_mount(
    tmp_path: Path,
) -> Path:
    """Create a file to mount."""
    extra_file_mount = tmp_path / "envs/extra.env"
    extra_file_mount.parent.mkdir()
    extra_file_mount.touch()
    return extra_file_mount


@pytest.fixture
def extra_dir_mount(
    tmp_path: Path,
) -> Path:
    """Create a directory to mount."""
    extra_dir_mount = tmp_path / "extra_dir"
    extra_dir_mount.mkdir()
    return extra_dir_mount


@pytest.fixture
def extra_mounts(
    extra_file_mount: Path,
    extra_dir_mount: Path,
) -> List[Dict[str, Any]]:
    """Create a list of extra mounts."""
    return [
        {
            "container-names": ["edgar-allen-poebot", "ot3-state-manager"],
            "host-path": str(extra_file_mount),
            "container-path": "/extra.env",
        },
        {
            "container-names": ["ot3-head", "emulator-proxy"],
            "host-path": str(extra_dir_mount),
            "container-path": "/extra_dir",
        },
    ]


@pytest.fixture
def extra_mounts_with_bad_container_names(
    extra_file_mount: Path,
    extra_dir_mount: Path,
) -> List[Dict[str, Any]]:
    """Create a list of extra mounts with bad container names."""
    return [
        {
            "container-names": ["no-bot", "ot3-state-imploder"],
            "host-path": str(extra_file_mount),
            "container-path": "/extra.env",
        },
        {
            "container-names": ["ot3-foot", "emulator-pixie"],
            "host-path": str(extra_dir_mount),
            "container-path": "/extra_dir",
        },
    ]


def test_extra_mounts(
    extra_file_mount: Path,
    extra_dir_mount: Path,
    extra_mounts: List[Dict[str, Any]],
    ot3_only: Dict[str, Any],
) -> None:
    """Test extra mounts added correctly"""
    ot3_only["extra-mounts"] = extra_mounts
    converted_object = convert_from_obj(ot3_only, dev=False)
    robot_server = converted_object.robot_server
    state_manager = converted_object.ot3_state_manager
    for container in [robot_server, state_manager]:
        assert container is not None
        assert mount_string_is(f"{str(extra_file_mount)}:/extra.env", container)

        assert not mount_string_is(f"{str(extra_dir_mount)}:/extra_dir", container)

    emulator_proxy = converted_object.emulator_proxy
    ot3_head = converted_object.ot3_head_emulator

    for container in [emulator_proxy, ot3_head]:
        assert container is not None
        assert not mount_string_is(f"{str(extra_file_mount)}:/extra.env", container)
        assert mount_string_is(f"{str(extra_dir_mount)}:/extra_dir", container)


def test_exception_thrown_on_invalid_container_names(
    extra_mounts_with_bad_container_names: List[Dict[str, Any]],
    ot3_only: Dict[str, Any],
) -> None:
    """Test that exception is thrown if extra mounts have invalid container names."""
    ot3_only["extra-mounts"] = extra_mounts_with_bad_container_names
    with pytest.raises(ValueError) as error_info:
        convert_from_obj(ot3_only, dev=False)

    assert (
        'The following "container_names" specified in "extra-mounts" do not exist in the emulated system:'
        in str(error_info.value)
    )
