"""Entrypoint for the emulation system cli application."""
from emulation_system.parsers.top_level_parser import TopLevelParser

if __name__ == "__main__":
    TopLevelParser().parse().execute()
