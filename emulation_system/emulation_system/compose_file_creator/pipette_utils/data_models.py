"""Data models for pipettes."""

import json
from dataclasses import dataclass
from datetime import datetime
from string import Template
from typing import Dict, List, Literal, Union

from emulation_system.compose_file_creator.pipette_utils.lookups import (
    OT2PipetteLookup,
    OT3PipetteLookup,
    PipetteRestrictions,
    PipetteTypes,
)
from emulation_system.consts import EEPROM_FILE_NAME

OT3_SERIAL_CODE_MIN_CHARS = 1
OT3_SERIAL_CODE_MAX_CHARS = 12
OT3_MODEL_MAX_VALUE = 99
OT3_MODEL_MIN_VALUE = 0
LEFT_PIPETTE_ENV_VAR_NAME = "LEFT_OT3_PIPETTE_DEFINITION"
RIGHT_PIPETTE_ENV_VAR_NAME = "RIGHT_OT3_PIPETTE_DEFINITION"


def _get_date_string() -> str:
    """Gets todays date string in the format of MMDDYYYY."""
    return datetime.now().strftime("%m%d%Y")


def _get_eeprom_file_name() -> str:
    """Gets eeprom file name."""
    # This is super simple for now and could probably just be a class var on PipetteInfo.
    # But I would rather follow the same pattern and make it easier to add logic to this down the line
    return EEPROM_FILE_NAME


def generate_eeprom_file_path(mount: Literal["left", "right"]) -> str:
    """Generates eeprom file path."""
    return f"/volumes/{mount}-pipette-eeprom/{_get_eeprom_file_name()}"

@dataclass
class PipetteInfo:
    """Class for pipette info."""

    display_name: str
    internal_name: str
    restrictions: List[PipetteRestrictions]
    pipette_type: PipetteTypes
    model: int
    serial_code: str
    eeprom_file_name: str


    @classmethod
    def from_pipette_lookup(cls, pipette_lookup: Union["OT2PipetteLookup", "OT3PipetteLookup"]) -> "PipetteInfo":
        """Creates pipette info from pipette lookup."""
        return cls(
            display_name=pipette_lookup.display_name,
            internal_name=pipette_lookup.pipette_name,
            restrictions=pipette_lookup.pipette_restrictions,
            pipette_type=pipette_lookup.pipette_type,
            model=pipette_lookup.get_pipette_model(),
            serial_code=_get_date_string(),
            eeprom_file_name=_get_eeprom_file_name(),
        )
    
    @classmethod
    def EMPTY(cls) -> "PipetteInfo":
        """Creates empty pipette info."""
        return cls(
            display_name="EMPTY",
            internal_name="EMPTY",
            restrictions=[],
            pipette_type=PipetteTypes.SINGLE,
            model=-1,
            serial_code="",
            eeprom_file_name=_get_eeprom_file_name()
        )

    @property
    def simulator_name(self) -> str:
        """Gets simulator name."""
        return self.pipette_type.get_simulator_name()

    def _validate_restrictions(self) -> None:
        """Validates restrictions."""
        pass


@dataclass
class RobotPipettes:
    """Class for robot pipettes."""

    left: PipetteInfo | None
    right: PipetteInfo | None

    def _validate_blocks_other_mount(self) -> None:
        """Validates pipettes that block other mount."""
        error_message_template = Template(
            "\nYou have specified both a right and a left pipette."
            '\nBut $blocking_pipette pipette: "$blocking_pipette_display_name", blocks both pipette mounts.'
            "\nPlease do one of the following:"
            "\n\t- Remove the $other_pipette pipette"
            "\n\t- Change your $blocking_pipette pipette."
        )
        left_pipette_blocks_other_mount = (
            self.left is not None
            and PipetteRestrictions.BLOCKS_OTHER_MOUNT in self.left.restrictions
        )
        right_pipette_blocks_other_mount = (
            self.right is not None
            and PipetteRestrictions.BLOCKS_OTHER_MOUNT in self.right.restrictions
        )

        if (
            self.left is not None
            and self.right is not None
            and left_pipette_blocks_other_mount
        ):
            raise ValueError(
                error_message_template.substitute(
                    blocking_pipette="left",
                    blocking_pipette_display_name=self.left.display_name,
                    other_pipette="right",
                )
            )

        if (
            self.left is not None
            and self.right is not None
            and right_pipette_blocks_other_mount
        ):
            raise ValueError(
                error_message_template.substitute(
                    blocking_pipette="right",
                    blocking_pipette_display_name=self.right.display_name,
                    other_pipette="left",
                )
            )

    def _validate_left_mount_only(self) -> None:
        """Validates pipettes that are left mount only."""
        if (
            self.right is not None
            and PipetteRestrictions.LEFT_MOUNT_ONLY in self.right.restrictions
        ):
            raise ValueError(
                f'"{self.right.display_name}" is restricted to left mount only. '
                "Please change the configuration file to have the pipette use the left mount."
            )

    def _validate_restrictions(self) -> None:
        """Validates robot pipettes."""
        self._validate_blocks_other_mount()

        if self.left is not None:
            self.left._validate_restrictions()

        if self.right is not None:
            self.right._validate_restrictions()
            self._validate_left_mount_only()

    def __post_init__(self) -> None:
        """Validates robot pipettes."""
        self._validate_restrictions()

    @staticmethod
    def _to_ot3_env_var(
        mount: Literal["left", "right"], pipette_info: PipetteInfo | None
    ) -> Dict[str, str]:
        """Converts to enviroment variable string."""
        env_var_name = (
            LEFT_PIPETTE_ENV_VAR_NAME if mount == "left" else RIGHT_PIPETTE_ENV_VAR_NAME
        )
        content: Dict[str, str | int] = {
            "eeprom_file_path": generate_eeprom_file_path(mount)
        }
        if pipette_info is None:
            pipette_info = PipetteInfo.EMPTY()

        content.update(
            {
                "pipette_name": pipette_info.internal_name,
                "pipette_model": pipette_info.model,
                "pipette_serial_code": pipette_info.serial_code,
                "eeprom_file_path": generate_eeprom_file_path(mount),
            }
        )

        return {env_var_name: json.dumps(content)}

    def get_left_pipette_env_var(self) -> Dict[str, str]:
        """Gets left pipette env var."""
        return self._to_ot3_env_var("left", self.left)

    def get_right_pipette_env_var(self) -> Dict[str, str]:
        """Gets right pipette env var."""
        return self._to_ot3_env_var("right", self.right)
