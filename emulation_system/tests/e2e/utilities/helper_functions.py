from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import docker
from docker.models.containers import Container

from emulation_system.compose_file_creator import Service


def get_volumes(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "volume"]


def get_mounts(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "bind"]


def named_volume_exists(
    container: Container, expected_name: str, expected_path: str
) -> bool:
    volumes = get_volumes(container)
    if volumes is None:
        return False
    filtered_volume = [
        volume
        for volume in volumes
        if (
                volume["Type"] == "volume"
                and volume["Name"] == expected_name
                and volume["Destination"] == expected_path
        )
    ]
    return len(filtered_volume) == 1


def mount_exists(container: Container, expected_src: str, expected_dest: str) -> bool:
    mounts = get_mounts(container)
    if mounts is None:
        return False
    filtered_mount = [
        mount
        for mount in mounts
        if (
                mount["Type"] == "bind"
                and mount["Source"] == expected_src
                and mount["Destination"] == expected_dest
        )
    ]
    return len(filtered_mount) == 1


def get_container(service: Service) -> Optional[Container]:
    if service is None:
        return
    else:
        return docker.from_env().containers.get(service.container_name)
