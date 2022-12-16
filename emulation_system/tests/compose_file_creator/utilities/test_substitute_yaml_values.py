"""Test that yaml substitution works."""

import pytest
import yaml

from emulation_system.compose_file_creator.utilities.substitute_yaml_values import (
    Substitution,
    YamlSubstitution,
)

SUB_LIST = [
    Substitution("otie", "source-location", "branch-name"),
    Substitution("otie", "exposed-port", "5000"),
]


@pytest.fixture
def remote_only_ot3() -> str:
    """Remote only OT-3 for testing."""
    return yaml.dump(
        {
            "robot": {
                "id": "otie",
                "hardware": "ot3",
                "emulation-level": "hardware",
                "source-type": "remote",
                "source-location": "latest",
                "robot-server-source-type": "remote",
                "robot-server-source-location": "latest",
                "opentrons-hardware-source-type": "remote",
                "opentrons-hardware-source-location": "latest",
                "can-server-source-type": "remote",
                "can-server-source-location": "latest",
                "exposed-port": 31950,
                "hardware-specific-attributes": {},
            }
        }
    )


def test_yaml_substitution(remote_only_ot3: str) -> None:
    """Confirm that yaml substitutions work correctly."""
    resultant_config_model = YamlSubstitution(
        remote_only_ot3, SUB_LIST
    ).perform_substitution()
    assert resultant_config_model.robot is not None
    assert resultant_config_model.robot.source_location == "branch-name"
    assert resultant_config_model.robot.exposed_port == 5000
