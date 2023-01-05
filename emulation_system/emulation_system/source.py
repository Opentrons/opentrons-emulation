"""Classes for interacting with source code.

Supports interaction with local or remote code.
"""

import os
import pathlib
import re
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

from emulation_system.compose_file_creator.config_file_settings import (
    FileMount,
    Hardware,
    MountTypes,
    OpentronsRepository,
    OT3Hardware,
    RepoToBuildArgMapping,
)
from emulation_system.consts import (
    COMMIT_SHA_REGEX,
    ENTRYPOINT_FILE_LOCATION,
    MONOREPO_NAMED_VOLUME_STRING,
)

ENTRYPOINT_MOUNT_STRING = FileMount(
    type=MountTypes.FILE,
    source_path=pathlib.Path(ENTRYPOINT_FILE_LOCATION),
    mount_path="/entrypoint.sh",
).get_bind_mount_string()


class SourceState(Enum):
    """State of Source object.

    Can either be local, remote latest, or remote commit.
    """

    REMOTE_LATEST = auto()
    REMOTE_COMMIT = auto()
    LOCAL = auto()

    @staticmethod
    def to_source_state(passed_value: str) -> "SourceState":
        """Helper method to parse passed string value to SourceState."""
        source_state: SourceState

        if passed_value.lower() == "latest":
            source_state = SourceState.REMOTE_LATEST
        elif re.match(COMMIT_SHA_REGEX, passed_value.lower()):
            source_state = SourceState.REMOTE_COMMIT
        elif os.path.isdir(passed_value):
            source_state = SourceState.LOCAL
        else:
            raise ValueError(
                f'\nYou passed: "{passed_value}"'
                "\nField can be the following values:"
                '\n\t- "latest" to pull latest code from Github'
                "\n\t- A valid commit sha to pull a specfic commit from Github"
                "\n\t- A valid absolute directory path to use your local code\n\n"
            )
        return source_state

    def is_remote(self) -> bool:
        """If SourceState is remote."""
        return self in [self.REMOTE_COMMIT, self.REMOTE_LATEST]

    def is_local(self) -> bool:
        """If SourceState is local."""
        return self == self.LOCAL


class Source(ABC):
    """ABC for Source objects."""

    source_location: str
    repo: OpentronsRepository

    def __init__(self, source_location: str, repo: OpentronsRepository) -> None:
        self.source_location = source_location
        self.repo = repo

    @classmethod
    @abstractmethod
    def validate(cls, v: str) -> "Source":
        """Required validate method to create custom Pydantic datatype."""
        ...

    @classmethod
    def __get_validators__(cls):  # noqa: ANN206
        """Required __get_validators__ method to create custom Pydantic datatype."""
        yield cls.validate

    @abstractmethod
    def generate_builder_mount_strings(self) -> List[str]:
        """Generates volume and bint mount strings for builder classes."""
        ...

    @property
    def source_state(self) -> SourceState:
        """Source State of the Source object."""
        return SourceState.to_source_state(self.source_location)

    @property
    def repo_to_build_arg_mapping(self) -> RepoToBuildArgMapping:
        """Build arg name for repo."""
        return RepoToBuildArgMapping.get_mapping(self.repo)

    def is_remote(self) -> bool:
        """Returns True if source is remote."""
        return self.source_state.is_remote()

    def is_local(self) -> bool:
        """Returns True is source is local."""
        return self.source_state.is_local()


class EmulatorSourceMixin:
    """Mixin providing functionality to classes that require evaluation of hardware type."""

    @staticmethod
    def generate_emulator_mount_strings_from_hw(
        emulator_hw: OT3Hardware | Hardware,
    ) -> List[str]:
        """Method to generate mount strings based off of hardware."""
        return [
            ENTRYPOINT_MOUNT_STRING,
            f"{emulator_hw.hw_name}_executable:/executable",
        ]


class MonorepoSource(Source):
    """Source class for opentrons monorepo."""

    def __init__(self, source_location: str) -> None:
        """Instantiate MonorepoSource object"""
        super().__init__(source_location, OpentronsRepository.OPENTRONS)

    @classmethod
    def validate(cls, v: str) -> "MonorepoSource":
        """Confirm that parsing source-location string to SourceState does not throw an error."""
        try:
            SourceState.to_source_state(v)
        except ValueError:
            raise
        else:
            return MonorepoSource(source_location=v)

    def __repr__(self) -> str:
        """Override __repr__."""
        return f"MonorepoSource({super().__repr__()})"

    @staticmethod
    def generate_emulator_mount_strings() -> List[str]:
        """Generates volume and bind mount strings for emulator contianers using monorepo source code."""
        return [ENTRYPOINT_MOUNT_STRING, MONOREPO_NAMED_VOLUME_STRING]

    def generate_builder_mount_strings(self) -> List[str]:
        """Generates volume and bind mount strings for LocalMonorepoBuilderBuilder container."""
        default_values = [MONOREPO_NAMED_VOLUME_STRING, ENTRYPOINT_MOUNT_STRING]

        if self.is_local():
            default_values.append(f"{self.source_location}:/{self.repo.value}")

        return default_values


class OT3FirmwareSource(Source, EmulatorSourceMixin):
    """Source class for opentrons ot3-firmware repo."""

    def __init__(self, source: str) -> None:
        """Instantiate OT3FirmwareSource object."""
        super().__init__(source, OpentronsRepository.OT3_FIRMWARE)

    @classmethod
    def validate(cls, v: str) -> "OT3FirmwareSource":
        """Confirm that parsing source-location string to SourceState does not throw an error."""
        try:
            SourceState.to_source_state(v)
        except ValueError:
            raise
        else:
            return OT3FirmwareSource(source=v)

    def __repr__(self) -> str:
        """Override __repr__."""
        return f"OT3FirmwareSource({super().__repr__()})"

    def generate_builder_mount_strings(self) -> List[str]:
        """Generates volume and bint mount strings for LocalOT3FirmwareBuilderBuilder container."""
        default_values = [
            f"{member.named_volume_name}:{member.container_volume_storage_path}"
            for member in OT3Hardware.__members__.values()
        ]

        default_values.append(ENTRYPOINT_MOUNT_STRING)
        if self.is_local():
            default_values.append(f"{self.source_location}:/{self.repo.value}")

        return default_values


class OpentronsModulesSource(Source, EmulatorSourceMixin):
    def __init__(self, source: str) -> None:
        super().__init__(source, OpentronsRepository.OPENTRONS_MODULES)

    @classmethod
    def validate(cls, v: str) -> "OpentronsModulesSource":
        try:
            SourceState.to_source_state(v)
        except ValueError:
            raise
        else:
            return OpentronsModulesSource(source=v)

    def __repr__(self):
        return f"OpentronsModulesSource({super().__repr__()})"

    def generate_builder_mount_strings(self) -> List[str]:
        """Method to generate volume and bint mount strings for builder classes."""
        default_values = [
            f"{hardware.named_volume_name}:{hardware.container_volume_storage_path}"
            for hardware in Hardware.opentrons_modules_hardware()
        ]
        default_values.append(ENTRYPOINT_MOUNT_STRING)

        if self.is_local():
            default_values.append(f"{self.source_location}:/{self.repo.value}")

        return default_values
