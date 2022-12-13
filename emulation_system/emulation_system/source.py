import os
import pathlib
import re
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List

from emulation_system.compose_file_creator.config_file_settings import (
    DirectoryMount,
    MountTypes,
    OpentronsRepository,
    RepoToBuildArgMapping,
)
from emulation_system.consts import COMMIT_SHA_REGEX


class SourceState(Enum):
    REMOTE_LATEST = auto()
    REMOTE_COMMIT = auto()
    LOCAL = auto()

    @staticmethod
    def parse_source_state(passed_value: str) -> "SourceState":
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
        return self in [self.REMOTE_COMMIT, self.REMOTE_LATEST]

    def is_local(self) -> bool:
        return self == self.LOCAL


class Source(ABC):
    source_location: str
    repo: OpentronsRepository

    def __init__(self, source_location: str, repo: OpentronsRepository) -> None:
        self.source_location = source_location
        self.repo = repo

    @classmethod
    @abstractmethod
    def validate(cls, v: str) -> "Source":
        ...

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @property
    def source_state(self) -> SourceState:
        return SourceState.parse_source_state(self.source_location)

    @property
    def repo_to_build_arg_mapping(self) -> RepoToBuildArgMapping:
        return RepoToBuildArgMapping.get_mapping(self.repo)

    def generate_mount_string(self) -> List[str]:
        service_mount_path = os.path.basename(os.path.normpath(self.source_location))
        return (
            [
                DirectoryMount(
                    type=MountTypes.DIRECTORY,
                    source_path=pathlib.Path(self.source_location),
                    mount_path=f"/{service_mount_path}",
                ).get_bind_mount_string()
            ]
            if self.source_state.is_local()
            else []
        )

    def is_remote(self) -> bool:
        return self.source_state.is_remote()

    def is_local(self) -> bool:
        return self.source_state.is_local()


class MonorepoSource(Source):
    def __init__(self, source: str) -> None:
        super().__init__(source, OpentronsRepository.OPENTRONS)

    @classmethod
    def validate(cls, v: str) -> "MonorepoSource":
        try:
            SourceState.parse_source_state(v)
        except ValueError:
            raise
        else:
            return MonorepoSource(source=v)

    def __repr__(self):
        return f"MonorepoSource({super().__repr__()})"


class OT3FirmwareSource(Source):
    def __init__(self, source: str) -> None:
        super().__init__(source, OpentronsRepository.OT3_FIRMWARE)

    @classmethod
    def validate(cls, v: str) -> "OT3FirmwareSource":
        try:
            SourceState.parse_source_state(v)
        except ValueError:
            raise
        else:
            return OT3FirmwareSource(source=v)

    def __repr__(self):
        return f"OT3FirmwareSource({super().__repr__()})"


class OpentronsModulesSource(Source):
    def __init__(self, source: str) -> None:
        super().__init__(source, OpentronsRepository.OPENTRONS_MODULES)

    @classmethod
    def validate(cls, v: str) -> "OpentronsModulesSource":
        try:
            SourceState.parse_source_state(v)
        except ValueError:
            raise
        else:
            return OpentronsModulesSource(source=v)

    def __repr__(self):
        return f"OpentronsModulesSource({super().__repr__()})"
