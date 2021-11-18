from __future__ import annotations
import json
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, parse_obj_as

class ConfigurationFileNotFoundError(FileNotFoundError):
    pass


class DefaultFolderPaths(BaseModel):
    opentrons: str = None
    ot3_firmware: str = Field(alias="ot3-firmware", default=None)
    modules: str = None


class GlobalSettings(BaseModel):
    default_folder_paths: DefaultFolderPaths = Field(..., alias="default-folder-paths")


class Heads(BaseModel):
    opentrons: str
    ot3_firmware: str = Field(..., alias="ot3-firmware")
    modules: str


class Commits(BaseModel):
    opentrons: str
    ot3_firmware: str = Field(..., alias="ot3-firmware")
    modules: str


class SourceDownloadLocations(BaseModel):
    heads: Heads
    commits: Commits


class EmulationSettings(BaseModel):
    source_download_locations: SourceDownloadLocations = Field(
        ..., alias="source-download-locations"
    )


class SharedFolder(BaseModel):
    host_path: str = Field(..., alias="host-path")
    vm_path: str = Field(..., alias="vm-path")


class VirtualMachineSettings(BaseModel):
    dev_vm_name: str = Field(..., alias="dev-vm-name")
    prod_vm_name: str = Field(..., alias="prod-vm-name")
    vm_memory: int = Field(..., alias="vm-memory")
    vm_cpus: int = Field(..., alias="vm-cpus")
    num_socket_can_networks: int = Field(..., alias="num-socket-can-networks")
    shared_folders: List[str] = Field(
        alias="shared-folders", default=[]
    )


class ConfigurationSettings(BaseModel):
    global_settings: GlobalSettings = Field(..., alias="global-settings")
    emulation_settings: EmulationSettings = Field(..., alias="emulation-settings")
    virtual_machine_settings: VirtualMachineSettings = Field(
        ..., alias="virtual-machine-settings"
    )
    aws_ecr_settings: Dict[str, Any] = Field(..., alias="aws-ecr-settings")

    @classmethod
    def from_file_path(cls, json_file_path: str) -> ConfigurationSettings:
        try:
            file = open(json_file_path, "r")
        except FileNotFoundError:
            raise ConfigurationFileNotFoundError(
                f"\nError loading configuration file.\n"
                f"Configuration file not found at: {json_file_path}\n"
                f"Please create a JSON configuration file"
            )

        return parse_obj_as(cls, json.load(file))
