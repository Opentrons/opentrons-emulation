"""Intermediate types that will be used for composing RuntimeComposeModel."""

from dataclasses import dataclass
from typing import Union

from emulation_system.compose_file_creator import Service

DockerServices = dict[str, Service]
IntermediateNetworks = list[str]
IntermediateVolumes = list[str]
IntermediatePorts = list[str]
IntermediateEnvironmentVariables = dict[str, Union[str, int, float]]
IntermediateDependsOn = list[str]
IntermediateCommand = list[str]
IntermediateBuildArgs = dict[str, str]


@dataclass
class IntermediateHealthcheck:
    """All values necessary for healthcheck."""

    interval: int
    retries: int
    timeout: int
    command: str
