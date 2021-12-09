from __future__ import annotations
from typing import Optional, Union, Dict
import json
import os.path
from compose_file_creator.input.models.container_types.thermocycler_module import ThermocyclerModuleAttributes
from compose_file_creator.input.models.container_types.temperature_module import TemperatureModuleAttributes
from emulation_system.consts import ROOT_DIR
CONFIG_FILE_LOCATION = os.path.join(ROOT_DIR, "emulation_system/resources/config.json")


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
    try:
        content = json.load(open(CONFIG_FILE_LOCATION, 'r'))
        hardware_list = parse_obj_as(List[ContainerModel], content['hardware'])
        for item in hardware_list:
            print(item)
    except ValidationError as e:
        print(e)