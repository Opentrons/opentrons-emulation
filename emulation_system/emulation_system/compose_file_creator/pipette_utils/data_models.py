"""Data models for pipettes."""

import json
from dataclasses import dataclass
from datetime import datetime
from string import Template
from typing import Dict, Union

from emulation_system.compose_file_creator.pipette_utils.lookups import (
    OT2PipetteLookup,
    OT3PipetteLookup,
    PipetteRestrictions,
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


@dataclass
class PipetteInfo:
    """Class for pipette info."""

    def __init__(
        self, pipette_lookup: Union["OT2PipetteLookup", "OT3PipetteLookup"]
    ) -> None:
        """Sets pipette info from pipette lookup."""
        self.display_name = pipette_lookup.display_name
        self.internal_name = pipette_lookup.pipette_name
        self.restrictions = pipette_lookup.pipette_restrictions
        self.model = self._format_model(pipette_lookup.get_pipette_model())
        self.serial_code = _get_date_string()
        self.eeprom_file_name = _get_eeprom_file_name()

    @staticmethod
    def _format_model(model: int) -> str:
        """Formats model attribute to a 0 padded string of length 2."""
        return str(model).zfill(2)

    def _to_ot3_env_var(self, env_var_name: str) -> Dict[str, str]:
        """Converts to enviroment variable string."""
        content = json.dumps(
            {
                "pipette_name": self.internal_name,
                "pipette_model": self.model,
                "pipette_serial_code": self.serial_code,
                "eeprom_file_name": self.eeprom_file_name,
            }
        )
        return {env_var_name: content}

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

    def get_left_pipette_env_var(self) -> Dict[str, str]:
        """Gets left pipette env var."""
        return (
            self.left._to_ot3_env_var(LEFT_PIPETTE_ENV_VAR_NAME)
            if self.left
            else {LEFT_PIPETTE_ENV_VAR_NAME: ""}
        )

    def get_right_pipette_env_var(self) -> Dict[str, str]:
        """Gets right pipette env var."""
        return (
            self.right._to_ot3_env_var(RIGHT_PIPETTE_ENV_VAR_NAME)
            if self.right
            else {RIGHT_PIPETTE_ENV_VAR_NAME: ""}
        )
