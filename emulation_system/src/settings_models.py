from __future__ import annotations
import json
from typing import Any, Dict

from pydantic import BaseModel, Field, parse_obj_as


class DefaultFolderPaths(BaseModel):
    opentrons: str
    ot3_firmware: str = Field(..., alias='ot3-firmware')
    modules: str


class GlobalSettings(BaseModel):
    default_folder_paths: DefaultFolderPaths = Field(..., alias='default-folder-paths')


class Heads(BaseModel):
    opentrons: str
    ot3_firmware: str = Field(..., alias='ot3-firmware')
    modules: str


class Commits(BaseModel):
    opentrons: str
    ot3_firmware: str = Field(..., alias='ot3-firmware')
    modules: str


class SourceDownloadLocations(BaseModel):
    heads: Heads
    commits: Commits


class EmulationSettings(BaseModel):
    source_download_locations: SourceDownloadLocations = Field(
        ..., alias='source-download-locations'
    )


class VirtualMachineSettings(BaseModel):
    dev_vm_name: str = Field(..., alias='dev-vm-name')
    prod_vm_name: str = Field(..., alias='prod-vm-name')
    vm_memory: int = Field(..., alias='vm-memory')
    vm_cpu: int = Field(..., alias='vm-cpu')


class ConfigurationSettings(BaseModel):
    global_settings: GlobalSettings = Field(..., alias='global-settings')
    emulation: EmulationSettings = Field(..., alias="emulation-settings")
    virtual_machine: VirtualMachineSettings = Field(..., alias='virtual-machine-settings')
    aws_ecr: Dict[str, Any] = Field(..., alias='aws-ecr-settings')

    @classmethod
    def from_file_path(cls, json_file_path: str) -> ConfigurationSettings:
        return parse_obj_as(cls, json.load(open(json_file_path, 'r')))
