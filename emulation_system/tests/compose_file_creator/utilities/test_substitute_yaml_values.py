"""Test that yaml substitution works."""
from typing import Callable

import yaml

from emulation_system.compose_file_creator.utilities.substitute_yaml_values import (
    Substitution,
    YamlSubstitution,
)

SUB_LIST = [
    Substitution("monorepo-source", "edge", None),
    Substitution("exposed-port", "5000", "edgar-allen-poebot"),
]


def test_yaml_substitution(make_config: Callable) -> None:
    """Confirm that yaml substitutions work correctly."""
    remote_only_ot3 = yaml.dump(make_config(robot="ot3"))
    resultant_config_model = YamlSubstitution(
        remote_only_ot3, SUB_LIST
    ).perform_substitution()
    assert resultant_config_model.robot is not None
    assert resultant_config_model.monorepo_source.source_location == "edge"
    assert resultant_config_model.robot.exposed_port == 5000


def test_yaml_export(make_config: Callable) -> None:
    """Confirm that exported yaml is correct."""
    remote_only_ot3 = yaml.dump(make_config(robot="ot3"))
    resultant_config_model = YamlSubstitution(
        remote_only_ot3, SUB_LIST
    ).perform_substitution()
    converted_yaml = yaml.safe_load(resultant_config_model.to_yaml())
    assert (
        converted_yaml["monorepo-source"] == "edge"
    )
    assert converted_yaml["robot"]["exposed-port"] == 5000
