"""Intermediate types that will be used for composing RuntimeComposeModel."""
from emulation_system.compose_file_creator import Service

DockerServices = dict[str, Service]
RequiredNetworks = list[str]
Volumes = list[str]
Ports = list[str]
EnvironmentVariables = dict[str, str]
DependsOn = list[str]
Command = str
