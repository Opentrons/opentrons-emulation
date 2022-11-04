"""Intermediate types that will be used for composing RuntimeComposeModel."""
from dataclasses import dataclass
from enum import Enum
from typing import Union

from emulation_system.compose_file_creator import Service


class DependsOnConditions(Enum):
    """Conditions for depends_on.

    https://docs.docker.com/compose/compose-file/#long-syntax-1
    """

    STARTED = "service_started"
    HEALTHY = "service_healthy"
    COMPLETED_SUCCESSFULLY = "service_completed_successfully"


@dataclass
class IntermediateHealthcheck:
    """All values necessary for healthcheck."""

    interval: int
    retries: int
    timeout: int
    command: str


DockerServices = dict[str, Service]
IntermediateNetworks = list[str]
IntermediateVolumes = list[str]
IntermediatePorts = list[str]
IntermediateEnvironmentVariables = dict[str, Union[str, int, float]]
IntermediateDependsOn = dict[str, DependsOnConditions]
IntermediateCommand = list[str]
IntermediateBuildArgs = dict[str, str]
