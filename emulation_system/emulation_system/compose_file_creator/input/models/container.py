from __future__ import annotations
from typing import Optional, Union, Dict
from pydantic import BaseModel, parse_obj_as, ValidationError
from compose_file_creator.input.models.container_types.heater_shaker_module import HeaterShakerModuleAttributes
from compose_file_creator.input.models.container_types.thermocycler_module import ThermocyclerModuleAttributes
from compose_file_creator.input.models.container_types.temperature_module import TemperatureModuleAttributes


class ContainerModel(BaseModel):
    name: Optional[str]
    attributes: Union[
        HeaterShakerModuleAttributes,
        ThermocyclerModuleAttributes,
        TemperatureModuleAttributes,
    ]

    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
        extra = "forbid"

    @classmethod
    def from_dict(cls, config_dict: Dict[str: str]) -> ContainerModel:
        return parse_obj_as(ContainerModel, config_dict)

if __name__ == "__main__":
    configs = [
        {
            "name": "Heater Shaker Test",

            "attributes": {
                "hardware": "Heater Shaker Module",
                "emulation-level": "firmware",
                "source-type": "remote",
                "source-location": "latest",
            }
        },
        {
            "name": "Thermocycler Test",

            "attributes": {
                "hardware": "Thermocycler Module",
                "emulation-level": "driver",
                "source-type": "remote",
                "source-location": "latest",
                "lid-temperature": {
                    "degrees-per-tick": 3.0
                }
            }
        },        {
            "name": "Temperature Module Test",

            "attributes": {
                "hardware": "Temperature Module",
                "emulation-level": "driver",
                "source-type": "remote",
                "source-location": "latest",
            }
        },
    ]
    for config in configs:
        try:
            print(parse_obj_as(ContainerModel, config))
        except ValidationError as e:
            print(e)