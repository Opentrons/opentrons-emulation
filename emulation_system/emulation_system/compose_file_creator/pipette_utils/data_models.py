"""Data models for pipettes."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Union

from emulation_system.compose_file_creator.pipette_utils.lookups import (
    OT2PipetteLookup,
    OT3PipetteLookup,
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
    serial_code: str = field(default_factory=_get_date_string)

    def __post_init__(self) -> None:
        """Validates pipette info."""
        if (
            self.serial_code is not None
            and len(self.serial_code) < OT3_SERIAL_CODE_MIN_CHARS
        ):
            raise ValueError("Serial code is too short. Min length is 1 character.")

        if (
            self.serial_code is not None
            and len(self.serial_code) > OT3_SERIAL_CODE_MAX_CHARS
        ):
            raise ValueError("Serial code is too long. Max length is 12 characters.")

        if self.serial_code is not None and not self.serial_code.isalnum():
            raise ValueError("Serial code must be alphanumeric.")

        if (
            OT3_MODEL_MIN_VALUE > int(self.model)
            or int(self.model) > OT3_MODEL_MAX_VALUE
        ):
            raise ValueError(
                f"Model value must be between {OT3_MODEL_MIN_VALUE} and {OT3_MODEL_MAX_VALUE}."
            )

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


@dataclass
class RobotPipettes:
    """Class for robot pipettes."""

    left: PipetteInfo | None
    right: PipetteInfo | None
