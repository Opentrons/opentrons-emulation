"""Entrypoint for the emulation system cli application."""

from emulation_system.opentrons_emulation_configuration import (
    load_opentrons_emulation_configuration_from_env,
)
from emulation_system.parsers.top_level_parser import TopLevelParser

if __name__ == "__main__":
    settings = load_opentrons_emulation_configuration_from_env()
    TopLevelParser(settings).parse().execute()
