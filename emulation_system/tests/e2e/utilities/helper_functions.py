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


def _filter_mounts(
    container: Container, expected_mount: ExpectedMount
) -> List[Dict[str, Any]]:
    mounts = get_mounts(container)
    assert mounts is not None, "mounts are None"
    return [
        mount
        for mount in mounts
        if (
                mount["Type"] == "bind"
                and mount["Source"] == expected_mount.SOURCE_PATH
                and mount["Destination"] == expected_mount.DEST_PATH
        )
    ]


def _filter_volumes(
    container: Container, expected_vol: ExpectedNamedVolume
) -> List[Dict[str, Any]]:
    volumes = get_volumes(container)
    assert volumes is not None, "volumes are None"
    filtered_volume = [
        volume
        for volume in volumes
        if (
                volume["Type"] == "volume"
                and volume["Name"] == expected_vol.VOLUME_NAME
                and volume["Destination"] == expected_vol.DEST_PATH
        )
    ]

    return filtered_volume


def confirm_named_volume_exists(
    container: Container, expected_vol: ExpectedNamedVolume
) -> None:
    assert len(_filter_volumes(container, expected_vol)) == 1


def confirm_named_volume_does_not_exist(
    container: Container, expected_vol: ExpectedNamedVolume
) -> None:
    assert len(_filter_volumes(container, expected_vol)) == 0


def confirm_mount_exists(container: Container, expected_mount: ExpectedMount) -> None:
    assert len(_filter_mounts(container, expected_mount)) == 1


def confirm_mount_does_not_exist(
    container: Container, expected_mount: ExpectedMount
) -> None:
    assert len(_filter_mounts(container, expected_mount)) == 0


def get_container(service: Service) -> Optional[Container]:
    if service is None:
        return
    else:
        return docker.from_env().containers.get(service.container_name)
