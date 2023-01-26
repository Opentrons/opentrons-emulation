from typing import (
    Any,
    Dict,
    List,
    Optional,
)

import docker
from docker.models.containers import Container

from e2e.utilities.consts import (
    ExpectedMount,
    ExpectedNamedVolume,
)
from emulation_system.compose_file_creator import Service


def get_volumes(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "volume"]


def get_mounts(container: Container) -> Optional[List[Dict[str, Any]]]:
    return [mount for mount in container.attrs["Mounts"] if mount["Type"] == "bind"]


def named_volume_exists(
    container: Container,
    expected_vol: ExpectedNamedVolume
    ) -> bool:
    volumes = get_volumes(container)
    if volumes is None:
        return False
    filtered_volume = [
        volume
        for volume in volumes
        if (
                volume["Type"] == "volume"
                and volume["Name"] == expected_vol.VOLUME_NAME
                and volume["Destination"] == expected_vol.DEST_PATH
        )
    ]

    num_volumes = len(filtered_volume)
    if num_volumes == 0:
        return False
    elif num_volumes == 1:
        return True
    else:
        raise ValueError("More than 1 volume matched filter.")


def mount_exists(container: Container, expected_mount: ExpectedMount) -> bool:
    mounts = get_mounts(container)
    if mounts is None:
        return False
    filtered_mount = [
        mount
        for mount in mounts
        if (
                mount["Type"] == "bind"
                and mount["Source"] == expected_mount.SOURCE_PATH
                and mount["Destination"] == expected_mount.DEST_PATH
        )
    ]

    num_mounts = len(filtered_mount)
    if num_mounts == 0:
        return False
    elif num_mounts == 1:
        return True
    else:
        raise ValueError("More than 1 mount matched filter.")


def get_container(service: Service) -> Optional[Container]:
    if service is None:
        return
    else:
        return docker.from_env().containers.get(service.container_name)
