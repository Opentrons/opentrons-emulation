"""Intermediate types that will be used for composing RuntimeComposeModel."""

from emulation_system.compose_file_creator import Service

DockerServices = dict[str, Service]
IntermediateNetworks = list[str]
IntermediateVolumes = list[str]
IntermediatePorts = list[str]
IntermediateEnvironmentVariables = dict[str, str]
IntermediateDependsOn = list[str]
IntermediateCommand = str
IntermediateBuildArgs = dict[str, str]
