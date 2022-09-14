"""Script to perform yaml substitutions to opentrons-emulation config files."""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import List

import yaml
from pydantic import parse_obj_as
from pydantic.utils import deepcopy

from emulation_system import SystemConfigurationModel


@dataclass
class Substitution:
    """Definition of what to substitute in yaml file."""

    service_name: str
    value_to_replace: str
    replacement_value: str


@dataclass
class YamlSubstitution:
    """Class containing functionality to perform yaml substitutions."""

    raw_string: str
    subs: List[Substitution]

    def perform_substitution(self) -> SystemConfigurationModel:
        """Substitute all values in sub and return new model."""
        system_config = parse_obj_as(
            SystemConfigurationModel, yaml.safe_load(self.raw_string)
        )

        copied_model = deepcopy(system_config)
        for sub in self.subs:
            setattr(
                copied_model.get_by_id(sub.service_name),
                sub.value_to_replace.replace("-", "_"),
                sub.replacement_value,
            )
        return copied_model


def parse_to_subs(args: str) -> List[Substitution]:
    """Parse passed json to a list of Substitution classes."""
    try:
        # Stripping literal \n here because it sometimes gets added by Github Actions
        parsed_json = json.loads(args.replace("\\n", ""))
    except json.decoder.JSONDecodeError:
        raise Exception("Error parsing json passed to subs arg.")
    except Exception:
        raise
    return [Substitution(*sub) for sub in parsed_json]


def main() -> SystemConfigurationModel:
    """Parse cli args and perform substitution."""
    parser = argparse.ArgumentParser("Substitute yaml values")
    parser.add_argument(
        "raw_string",
        metavar="<yaml_input>",
        type=argparse.FileType("r"),
        nargs="?",
        help="Yaml string to modify",
        default=sys.stdin,
    )

    parser.add_argument(
        "subs",
        type=parse_to_subs,
        help="value to replace",
    )

    args = parser.parse_args(sys.argv[1:])
    args.raw_string = args.raw_string.read()
    parsed_yaml = YamlSubstitution(**vars(args))
    return parsed_yaml.perform_substitution()


if __name__ == "__main__":
    print(yaml.dump(main().dict(by_alias=True)))
