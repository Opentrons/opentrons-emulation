"""Pipette lookups Enums."""

import json
from enum import Enum, auto, unique
from typing import Generator, Literal, Tuple

from emulation_system.consts import PIPETTE_VERSIONS_FILE_PATH


class PipetteTypes(Enum):
    """Enum for pipette types."""

    SINGLE = auto()
    MULTI = auto()
    CHANNEL_96 = auto()


class BasePipetteLookup(Enum):
    """Base class for pipette enums.

    Provides lookup by name functionality and valid pipette name enum for use with Pydantic.
    """

    def __init__(
        self, display_name: str, pipette_name: str, pipette_type: PipetteTypes
    ) -> None:
        self.display_name = display_name
        self.pipette_name = pipette_name
        self.pipette_type = pipette_type

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
    # So we are addressing this by telling mypy to be quiet by using # type: ignore[valid-type] and
    # moving on with our very long day.

    @classmethod
    def _get_pipette_names(cls) -> Generator[Tuple[str, str], None, None]:
        for i, seq in enumerate(cls.__members__.items(), start=1):
            _, pipette_info = seq
            first_name = f"NAME_{(i * 2) - 1}"
            second_name = f"NAME_{(i * 2)}"

            yield from [
                (first_name, pipette_info.display_name),
                (second_name, pipette_info.pipette_name),
            ]

    @classmethod
    def get_valid_pipette_names(cls) -> Enum:
        """Returns enum with valid pipette names for use with Pydantic."""
        key_value_pairs = list(cls._get_pipette_names())
        return Enum(f"{cls.__name__}ValidNames", key_value_pairs, type=str)

    def _get_pipette_model(self, robot_type: Literal["ot2", "ot3"]) -> int:
        with open(PIPETTE_VERSIONS_FILE_PATH, "r") as file:
            versions = json.load(file)
        return versions[robot_type][self.pipette_name]


@unique
class OT2PipetteLookup(BasePipetteLookup):
    """Enum for OT-2 pipettes."""

    P20_SINGLE = ("P20 Single", "p20_single_gen2", PipetteTypes.SINGLE)
    P20_MULTI = ("P20 Multi", "p20_multi_gen2", PipetteTypes.MULTI)
    P300_SINGLE = ("P300 Single", "p300_single_gen2", PipetteTypes.SINGLE)
    P300_MULTI = ("P300 Multi", "p300_multi_gen2", PipetteTypes.MULTI)
    P1000_SINGLE_GEN2 = ("P1000 Single", "p1000_single_gen2", PipetteTypes.SINGLE)

    def __init__(
        self, display_name: str, pipette_name: str, pipette_type: PipetteTypes
    ) -> None:
        """Raises error if pipette type is 96 channel."""
        if pipette_type == PipetteTypes.CHANNEL_96:
            raise ValueError("OT-2 does not support 96 channel pipettes.")

        super().__init__(display_name, pipette_name, pipette_type)

    def get_pipette_model(self) -> int:
        """Gets pipette model."""
        return self._get_pipette_model("ot2")


@unique
class OT3PipetteLookup(BasePipetteLookup):
    """Enum for OT-3 pipettes."""

    P50_SINGLE = ("P50 Single", "p50_single_gen3", PipetteTypes.SINGLE)
    P50_MULTI = ("P50 Multi", "p50_multi_gen3", PipetteTypes.MULTI)
    P1000_SINGLE = ("P1000 Single", "p1000_single_gen3", PipetteTypes.SINGLE)
    P1000_MULTI = ("P1000 Multi", "p1000_multi_gen3", PipetteTypes.MULTI)
    P1000_96 = ("P1000 96 Channel", "p1000_96", PipetteTypes.CHANNEL_96)

    def get_pipette_model(self) -> int:
        """Gets pipette model."""
        return self._get_pipette_model("ot3")
