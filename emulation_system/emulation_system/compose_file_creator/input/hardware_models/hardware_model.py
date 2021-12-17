"""Parent class for all hardware."""
import os
import re
from typing import (
    Any,
    Dict,
    Pattern,
)

from pydantic import (
    BaseModel,
    Field,
    validator,
)

from emulation_system.compose_file_creator.config_file_settings import (
    EmulationLevel,
    Images,
    SourceRepositories,
    SourceType,
)


class HardwareModel(BaseModel):
    """Parent class of all hardware. Define attributes common to all hardware."""

    _ID_REGEX_FORMAT: Pattern = re.compile(r"^[a-zA-Z0-9-_]+$")

    source_type: SourceType = Field(alias="source-type")
    source_location: str = Field(alias="source-location")
    hardware: str
    id: str
    images: Images
    source_repos: SourceRepositories
    emulation_level: EmulationLevel = Field(alias="emulation-level")

    class Config:
        """Config class used by pydantic."""

        allow_population_by_field_name = True
        validate_assignment = True
        use_enum_values = True
        extra = "forbid"

    @validator("id")
    def check_id_format(cls, v: str) -> str:
        """Verifies that id matches expected format."""
        assert cls._ID_REGEX_FORMAT.match(v), (
            f'"{v}" does not match required format of only alphanumeric characters, '
            f"dashes and underscores"
        )
        return v

    @validator("source_location")
    def check_source_location(cls, v: str, values: Dict[str, Any]) -> str:
        """If source type is local, confirms directory path specified exists."""
        if values["source_type"] == SourceType.LOCAL:
            assert os.path.isdir(v), f'"{v}" is not a valid directory path'
        return v

    # @validator('emulation_level')
    # def confirm_valid_configuration(cls, v):  # noqa: ANN001, ANN201
    #     """Confirm that an emulator is defined for the passed hardware model."""
    #     source_repo = cls._hardware_definition.get_source_repo(v)
    #     hardware_type = cls._hardware_definition.id
    #     valid_configs = " and ".join(
    #         f"\"{config}\""
    #         for config
    #         in cls._hardware_definition.get_valid_configurations()
    #     )
    #     assert source_repo is not None, f"\"{hardware_type}\" does not have a " \
    #                                     f"\"{v}\" emulator defined. Valid " \
    #                                     f"configurations are {valid_configs}"
    #
    #     return v

    def get_image_name(self) -> str:
        """Get image name to run based off of class structure."""
        if (self.emulation_level == EmulationLevel.HARDWARE
                and self.source_type == SourceType.REMOTE):
            image_name = self.images.remote_hardware_image_name

        elif (self.emulation_level == EmulationLevel.HARDWARE
              and self.source_type == SourceType.LOCAL):
            image_name = self.images.local_hardware_image_name

        elif (self.emulation_level == EmulationLevel.FIRMWARE
                and self.source_type == SourceType.REMOTE):
            image_name = self.images.remote_firmware_image_name

        elif (self.emulation_level == EmulationLevel.FIRMWARE
              and self.source_type == SourceType.LOCAL):
            image_name = self.images.local_firmware_image_name

        return image_name

    def get_source_repo(self) -> str:
        """Get name of Docker image to use."""
        return "Hello World"
