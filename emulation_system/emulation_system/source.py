"""Classes for interacting with source code.

Supports interaction with local or remote code.
"""

import os
import pathlib
import re
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List, Union

from pydantic import Field

from emulation_system import github_api_interaction
from emulation_system.compose_file_creator.config_file_settings import (
    FileMount,
    Hardware,
    MountTypes,
    OpentronsRepository,
    OT3Hardware,
)
from emulation_system.compose_file_creator.types.intermediate_types import (
    IntermediateBuildArgs,
)
from emulation_system.consts import (
    COMMIT_SHA_REGEX,
    EMULATOR_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
    EMULATOR_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
    ENTRYPOINT_FILE_LOCATION,
    MONOREPO_NAMED_VOLUME_STRING,
    OPENTRONS_MODULES_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
    OPENTRONS_MODULES_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME,
    OT3_FIRMWARE_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
    OT3_FIRMWARE_BUILDER_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
    OT3_FIRMWARE_BUILDER_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
    OT3_FIRMWARE_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME,
)
from opentrons_pydantic_base_model import OpentronsBaseModel

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
    REMOTE_REF = auto()
    LOCAL = auto()

    @staticmethod
    def to_source_state(passed_value: str, repo: OpentronsRepository) -> "SourceState":
        """Helper method to parse passed string value to SourceState."""
        source_state: SourceState

        if passed_value.lower() == "latest":
            source_state = SourceState.REMOTE_LATEST
        elif os.path.isdir(passed_value):
            source_state = SourceState.LOCAL
        elif (
            github_api_interaction.github_api_is_up()
            and github_api_interaction.check_if_ref_exists(
                repo.OWNER,
                repo.value,
                passed_value,
            )
        ):
            source_state = SourceState.REMOTE_REF
        elif re.match(COMMIT_SHA_REGEX, passed_value.lower()):
            raise ValueError(
                "Usage of a commit SHA as a reference for a source location "
                "is deprecated. Use a branch name instead."
            )
        else:
            raise ValueError(
                f'\nYou passed: "{passed_value}"'
                "\nField can be the following values:"
                '\n\t- "latest" to pull latest code from Github'
                "\n\t- A valid ref name to pull a specific ref from Github"
                "\n\t- A valid absolute directory path to use your local code\n\n"
            )
        return source_state

    def is_remote(self) -> bool:
        """If SourceState is remote."""
        return self in [self.REMOTE_REF, self.REMOTE_LATEST]

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
        return SourceState.to_source_state(self.source_location, self.repo)

    def generate_build_args(self) -> IntermediateBuildArgs | None:
        """Generate build args based off of global settings."""
        if self.is_local():
            return None
        env_var_to_use = str(self.repo.build_arg_name)
        source_location = self.source_location
        value = (
            self.repo.get_default_download_url()
            if source_location == "latest"
            else self.repo.get_user_specified_download_url(source_location)
        )
        return {env_var_to_use: value}

    def generate_source_code_bind_mounts(self) -> List[str]:
        """Creates bind mounts that connect local code from host to container."""
        return [f"{self.source_location}:/{self.repo.value}"] if self.is_local() else []

    def is_remote(self) -> bool:
        """Returns True if source is remote."""
        return self.source_state.is_remote()

    def is_local(self) -> bool:
        """Returns True is source is local."""
        return self.source_state.is_local()


class EmulatorSourceMixin:
    """Mixin providing functionality to classes that require evaluation of hardware type."""

    @staticmethod
    def generate_emulator_executable_mount_strings_from_hw(
        emulator_hw: OT3Hardware | Hardware,
    ) -> List[str]:
        """Method to generate mount strings based off of hardware."""
        return [
            ENTRYPOINT_MOUNT_STRING,
            f"{emulator_hw.hw_name}-executable:/executable",
        ]


class MonorepoSource(OpentronsBaseModel, Source):
    """Source class for opentrons monorepo."""

    source_location: str
    repo: OpentronsRepository = OpentronsRepository.OPENTRONS
    DEFAULT_BUILDER_VOLUMES: List[str] = Field(
        [MONOREPO_NAMED_VOLUME_STRING], const=True
    )

    @classmethod
    def validate(cls, v: str) -> "MonorepoSource":
        """Confirm that parsing source-location string to SourceState does not throw an error."""
        try:
            SourceState.to_source_state(v, OpentronsRepository.OPENTRONS)
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
        return self.generate_source_code_bind_mounts() + self.DEFAULT_BUILDER_VOLUMES


class OT3FirmwareSource(OpentronsBaseModel, Source, EmulatorSourceMixin):
    """Source class for opentrons ot3-firmware repo."""

    source_location: str
    repo: OpentronsRepository = OpentronsRepository.OT3_FIRMWARE
    DEFAULT_BUILDER_VOLUMES: List[str] = Field(
        [
            OT3_FIRMWARE_BUILDER_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
            OT3_FIRMWARE_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
            OT3_FIRMWARE_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME,
            OT3_FIRMWARE_BUILDER_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
        ],
        const=True,
    )

    @staticmethod
    def _generate_emulator_executable_volumes() -> List[str]:
        return [
            f"{member.executable_volume_name}:{member.builder_executable_volume_path}"
            for member in OT3Hardware.__members__.values()
        ]

    @staticmethod
    def generate_emulator_eeprom_mount_strings_from_hw(
        emulator_hw: OT3Hardware,
    ) -> str:
        """Method to generate mount strings based off of OT3Hardware."""
        return f"{emulator_hw.eeprom_file_volume_name}:/eeprom"

    @staticmethod
    def _generate_builder_eeprom_mount_strings() -> List[str]:
        return [
            f"{member.eeprom_file_volume_name}:{member.eeprom_file_volume_storage_path}"
            for member in OT3Hardware.eeprom_required_hardware()
        ]

    @classmethod
    def validate(cls, v: str) -> "OT3FirmwareSource":
        """Confirm that parsing source-location string to SourceState does not throw an error."""
        try:
            SourceState.to_source_state(v, OpentronsRepository.OT3_FIRMWARE)
        except ValueError:
            raise
        else:
            return OT3FirmwareSource(source_location=v)

    def __repr__(self) -> str:
        """Override __repr__."""
        return f"OT3FirmwareSource({super().__repr__()})"

    def generate_builder_mount_strings(self) -> List[str]:
        """Generates volume and bind mount strings for LocalOT3FirmwareBuilderBuilder container."""
        return (
            self.DEFAULT_BUILDER_VOLUMES
            + self._generate_emulator_executable_volumes()
            + self.generate_source_code_bind_mounts()
            + self._generate_builder_eeprom_mount_strings()
        )

    @staticmethod
    def generate_state_manager_mount_strings() -> List[str]:
        """Generate mount strings specific to state_manager."""
        return [
            EMULATOR_STATE_MANAGER_VENV_NAMED_VOLUME_STRING,
            EMULATOR_STATE_MANAGER_WHEEL_NAMED_VOLUME_STRING,
        ]


class OpentronsModulesSource(OpentronsBaseModel, Source, EmulatorSourceMixin):
    """Source class for opentrons opentrons-modules repo."""

    source_location: str
    repo: OpentronsRepository = OpentronsRepository.OPENTRONS_MODULES
    DEFAULT_BUILDER_VOLUMES: List[str] = Field(
        [
            OPENTRONS_MODULES_BUILDER_BUILD_HOST_CACHE_OVERRIDE_VOLUME,
            OPENTRONS_MODULES_BUILDER_STM32_TOOLS_CACHE_OVERRIDE_VOLUME,
        ],
        const=True,
    )

    @staticmethod
    def _generate_emulator_executable_volumes() -> List[str]:
        return [
            f"{hardware.executable_volume_name}:{hardware.builder_executable_volume_path}"
            for hardware in Hardware.opentrons_modules_hardware()
        ]

    def _generate_necessary_bind_mounts(self) -> List[str]:
        return [f"{self.source_location}:/{self.repo.value}"] if self.is_local() else []

    @classmethod
    def validate(cls, v: str) -> "OpentronsModulesSource":
        """Confirm that parsing source-location string to SourceState does not throw an error."""
        try:
            SourceState.to_source_state(v, OpentronsRepository.OPENTRONS_MODULES)
        except ValueError:
            raise
        else:
            return OpentronsModulesSource(source_location=v)

    def __repr__(self) -> str:
        """Override __repr__."""
        return f"OpentronsModulesSource({super().__repr__()})"

    def generate_builder_mount_strings(self) -> List[str]:
        """Method to generate volume and bint mount strings for builder classes."""
        return (
            self.DEFAULT_BUILDER_VOLUMES
            + self._generate_emulator_executable_volumes()
            + self._generate_necessary_bind_mounts()
        )


OpentronsSource = Union[MonorepoSource, OpentronsModulesSource, OT3FirmwareSource]
