"""Script to perform yaml substitutions to opentrons-emulation config files."""

import argparse
import json
import sys
from dataclasses import dataclass
from typing import List, Optional

import yaml
from pydantic import parse_obj_as

from emulation_system import SystemConfigurationModel
from emulation_system.source import OpentronsSource


@dataclass
class Substitution:
    """Definition of what to substitute in yaml file."""

    value_to_replace: str
    replacement_value: str
    service_name: Optional[str] = None


@dataclass
class YamlSubstitution:
    """Class containing functionality to perform yaml substitutions."""

    raw_string: str
    subs: List[Substitution]

    def __replace_val(
        self, model_wip: SystemConfigurationModel, sub: Substitution
    ) -> None:
        obj_to_replace_on = (
            model_wip.get_by_id(sub.service_name)
            if sub.service_name is not None
            else model_wip
        )
        val_to_replace_w_underscores = sub.value_to_replace.replace("-", "_")

        if sub.value_to_replace in model_wip.source_repo_field_aliases:
            source_obj: OpentronsSource = getattr(
                obj_to_replace_on, val_to_replace_w_underscores
            )
            source_obj.source_location = sub.replacement_value

        else:
            setattr(
                obj_to_replace_on,
                val_to_replace_w_underscores,
                sub.replacement_value,
            )

    def perform_substitution(self) -> SystemConfigurationModel:
        """Substitute all values in sub and return new model."""
        system_config = parse_obj_as(
            SystemConfigurationModel, yaml.safe_load(self.raw_string)
        )

        copied_model = system_config.copy(deep=True)
        for sub in self.subs:
            self.__replace_val(copied_model, sub)
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

    print(main().to_yaml())
