"""Intermediate types that will be used for composing RuntimeComposeModel."""
from dataclasses import dataclass
from typing import Dict

from emulation_system.compose_file_creator.output.compose_file_model import Service


@dataclass
class DockerServices:
    """All services to be created by Docker."""

    services: Dict[str, Service]


@dataclass
class TopLevelNetworks:
    """Top level network definitions to be added to Compose file."""

    networks: Dict[str, None]


RequiredNetworks = list[str]
Volumes = list[str]
Ports = list[str]
EnvironmentVariables = dict[str, str]
DependsOn = list[str]
Command = str
