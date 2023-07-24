"""Tests related to extra-mounts on services"""

from pathlib import Path
from typing import Any, Dict

from emulation_system.compose_file_creator.conversion.conversion_functions import (
    convert_from_obj,
)
from tests.validation_helper_functions import mount_string_is


def test_extra_mounts(tmp_path: Path, ot3_only: Dict[str, Any]) -> None:
    """Test extra mounts added correctly"""
    extra_file_mount = tmp_path / "envs/extra.env"
    extra_file_mount.parent.mkdir()
    extra_file_mount.touch()
    
    extra_dir_mount = tmp_path / "extra_dir"
    extra_dir_mount.mkdir()

    ot3_only["extra-mounts"] = [
        {
            "container-names": ["edgar-allen-poebot", "ot3-state-manager"],
            "host-path": str(extra_file_mount),
            "container-path": "/extra.env",
        },
        {
            "container-names": ["ot3-head", "emulator-proxy"],
            "host-path": str(extra_dir_mount),
            "container-path": "/extra_dir",
        }
    ]

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
