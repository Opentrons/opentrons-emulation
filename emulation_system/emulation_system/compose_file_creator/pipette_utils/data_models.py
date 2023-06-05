"""Data models for pipettes."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from string import Template
from typing import Dict, List, Union

from emulation_system.compose_file_creator.pipette_utils.lookups import (
    OT2PipetteLookup,
    OT3PipetteLookup,
    PipetteRestrictions,
)

OT3_SERIAL_CODE_MIN_CHARS = 1
OT3_SERIAL_CODE_MAX_CHARS = 12
OT3_MODEL_MAX_VALUE = 99
OT3_MODEL_MIN_VALUE = 0
OT3_ENV_VAR_NAME = "OT3_PIPETTE_DEFINITION"


def _get_date_string() -> str:
    """Gets todays date string in the format of MMDDYYYY."""
    return datetime.now().strftime("%m%d%Y")


@dataclass
class PipetteInfo:
    """Class for pipette info."""

    display_name: str
    internal_name: str
    model: str
    restrictions: List[PipetteRestrictions]
    serial_code: str = field(default_factory=_get_date_string)

    @staticmethod
    def _format_model(model: int) -> str:
        """Formats model attribute to a 0 padded string of length 2."""
        return str(model).zfill(2)

    @classmethod
    def from_pipette_lookup_value(
        cls, pipette_lookup: Union["OT2PipetteLookup", "OT3PipetteLookup"]
    ) -> "PipetteInfo":
        """Sets pipette info from pipette lookup."""
        return cls(
            display_name=pipette_lookup.display_name,
            internal_name=pipette_lookup.pipette_name,
            restrictions=pipette_lookup.pipette_restrictions,
            model=cls._format_model(pipette_lookup.get_pipette_model()),
        )

    def to_ot3_env_var(self) -> Dict[str, str]:
        """Converts to enviroment variable string."""
        content = json.dumps(
            {
                "pipette_name": self.internal_name,
                "pipette_model": self.model,
                "pipette_serial_code": self.serial_code,
            }
        )
        return {OT3_ENV_VAR_NAME: content}

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
