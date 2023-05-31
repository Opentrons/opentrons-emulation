"""Module for pipette utilities."""

import datetime
import json
from dataclasses import dataclass
from enum import Enum, auto, unique
from typing import Any, ClassVar, Dict

from emulation_system.consts import PIPETTE_VERSIONS_FILE_PATH

OT3_SERIAL_CODE_MIN_CHARS = 1
OT3_SERIAL_CODE_MAX_CHARS = 12
OT3_MODEL_MAX_VALUE = 99
OT3_MODEL_MIN_VALUE = 0


class PipetteTypes(Enum):
    """Enum for pipette types."""

    SINGLE = auto()
    MULTI = auto()
    CHANNEL_96 = auto()


@dataclass(frozen=True)
class OT3EnvironmentVariableDefinition:
    """Class for OT-3 environment variable definitions."""

    pipette_name: str
    pipette_model: int
    pipette_serial_code: str | None
    variable_name: ClassVar[str] = "OT3_PIPETTE_DEFINITION"

    def _format_model(self) -> str:
        """Formats model attribute to a 0 padded string of length 2."""
        return str(self.pipette_model).zfill(2)

    @staticmethod
    def _get_date_string() -> str:
        """Gets todays date string in the format of MMDDYYYY."""
        return datetime.datetime.now().strftime("%m%d%Y")

    def to_env_var(self) -> Dict[str, str]:
        """Converts to enviroment variable string."""
        content = json.dumps(
            {
                "pipette_name": self.pipette_name,
                "pipette_model": self._format_model(),
                "pipette_serial_code": self.pipette_serial_code
                or self._get_date_string(),
            }
        )
        return {self.variable_name: content}


class BasePipetteEnum(Enum):
    """Base class for pipette enums.

    Provides lookup by name functionality and valid pipette name enum for use with Pydantic.
    """

    def __init__(self, pipette_name: str, pipette_type: PipetteTypes) -> None:
        self.pipette_name = pipette_name
        self.pipette_type = pipette_type

    def _get_pipette_versions_dict(self) -> Dict[str, Any]:
        """Gets pipette version."""
        with open(PIPETTE_VERSIONS_FILE_PATH, "r") as file:
            return json.load(file)

    @classmethod
    def lookup_by_name(cls, name: str) -> "BasePipetteEnum":
        """Looks up enum by name."""
        for _, pipette_info in cls.__members__.items():
            if pipette_info.pipette_name == name:
                return pipette_info
        raise ValueError(f"Pipette with name {name} not found.")

    ############################################
    # NOTE: This is WEIRD. Lets talk about it. #
    ############################################

    # This is a class method that returns an Enum using the Functional API.
    # https://docs.python.org/3.10/library/enum.html#functional-api

    # We want to construct an enum whose values are the pipette_name values from classes that subclass
    # this class
    # This method is called inside of input/hardware_models/robots/ot2_model.py and
    # input/hardware_models/robots/ot3_model.py. Mypy is not happy with this because it doesn't
    # like the fact that we are calling a method to define the types.
    # So we are address this by telling mypy to be quiet by using # type: ignore[valid-type] and
    # moving on with our very long day.

    @classmethod
    def valid_pipette_name_enum(cls) -> Enum:
        """Returns enum with valid pipette names for use with Pydantic."""
        key_value_pairs = [
            (f"{pipette_info.pipette_name.upper()}_NAME", pipette_info.pipette_name)
            for _, pipette_info in cls.__members__.items()
        ]
        return Enum(f"{cls.__name__}ValidNames", key_value_pairs, type=str)


@unique
class OT2Pipettes(BasePipetteEnum):
    """Enum for OT-2 pipettes."""

    P20_SINGLE = ("p20_single_gen2", PipetteTypes.SINGLE)
    P20_MULTI = ("p20_multi_gen2", PipetteTypes.MULTI)
    P300_SINGLE = ("p300_single_gen2", PipetteTypes.SINGLE)
    P300_MULTI = ("p300_multi_gen2", PipetteTypes.MULTI)
    P1000_SINGLE_GEN2 = ("p1000_single_gen2", PipetteTypes.SINGLE)

    def __init__(self, pipette_name: str, pipette_type: PipetteTypes) -> None:
        """Raises error if pipette type is 96 channel."""
        super().__init__(pipette_name, pipette_type)
        if self.pipette_type == PipetteTypes.CHANNEL_96:
            raise ValueError("OT-2 does not support 96 channel pipettes.")

    def get_pipette_version(self) -> int:
        """Gets pipette version."""
        return self._get_pipette_versions_dict()["ot2"][self.pipette_name]


@unique
class OT3Pipettes(BasePipetteEnum):
    """Enum for OT-3 pipettes."""

    P50_SINGLE = ("p50_single_gen3", PipetteTypes.SINGLE)
    P50_MULTI = ("p50_multi_gen3", PipetteTypes.MULTI)
    P1000_SINGLE = ("p1000_single_gen3", PipetteTypes.SINGLE)
    P1000_MULTI = ("p1000_multi_gen3", PipetteTypes.MULTI)
    P1000_96 = ("p1000_96", PipetteTypes.CHANNEL_96)

    def get_pipette_version(self) -> int:
        """Gets pipette version."""
        return self._get_pipette_versions_dict()["ot3"][self.pipette_name]

    def generate_pipette_env_var_def(
        self, model: int, serial_code: str | None
    ) -> OT3EnvironmentVariableDefinition:
        """Generates pipette serial code."""
        if serial_code is not None and len(serial_code) < OT3_SERIAL_CODE_MIN_CHARS:
            raise ValueError("Serial code is too short. Min length is 1 character.")

        if serial_code is not None and len(serial_code) > OT3_SERIAL_CODE_MAX_CHARS:
            raise ValueError("Serial code is too long. Max length is 12 characters.")

        if serial_code is not None and not serial_code.isalnum():
            raise ValueError("Serial code must be alphanumeric.")

        if OT3_MODEL_MIN_VALUE > model or model > OT3_MODEL_MAX_VALUE:
            raise ValueError(
                f"Model value must be between {OT3_MODEL_MIN_VALUE} and {OT3_MODEL_MAX_VALUE}."
            )

        return OT3EnvironmentVariableDefinition(
            pipette_name=self.pipette_name,
            pipette_model=model,
            pipette_serial_code=serial_code,
        )
