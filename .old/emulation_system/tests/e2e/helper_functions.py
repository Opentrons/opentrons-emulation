"""Module containing pure functions to retrieve general information from Docker containers."""

from typing import Dict, Iterable, List, Optional, Set

import docker  # type: ignore[import]
from docker.errors import NotFound as ContainerNotFoundError  # type: ignore[import]
from docker.models.containers import Container  # type: ignore[import]

from emulation_system.compose_file_creator import Service
from tests.e2e.consts import BindMountInfo, NamedVolumeInfo


def get_volumes(container: Optional[Container]) -> Set[NamedVolumeInfo]:
    """Gets a list of volumes for a docker container.

    Returns None if no volumes exist
    """
    return (
        set([])
        if container is None
        else {
            NamedVolumeInfo(VOLUME_NAME=mount["Name"], DEST_PATH=mount["Destination"])
            for mount in container.attrs["Mounts"]
            if mount["Type"] == "volume"
        }
    )


def get_mounts(container: Optional[Container]) -> Set[BindMountInfo]:
    """Gets a list of mounts for a docker container.

    Returns None if no mounts exist
    """
    return (
        set([])
        if container is None
        else {
            BindMountInfo(SOURCE_PATH=mount["Source"], DEST_PATH=mount["Destination"])
            for mount in container.attrs["Mounts"]
            if mount["Type"] == "bind"
        }
    )


def get_environment_variables(container: Optional[Container]) -> Dict[str, str]:
    """Gets a list of environment variables for a docker container.

    Returns None if no environment variables exist
    """
    if container is None:
        return {}
    else:
        env_var_list = container.attrs["Config"]["Env"]
        return {
            env_var.split("=")[0]: env_var.split("=")[1] for env_var in env_var_list
        }


def get_container_names(containers: Iterable[Container]) -> Set[str]:
    """Get set of container names given an iterable of containers."""
    return set([container.name for container in containers])


def get_container(service: Optional[Service]) -> Optional[Container]:
    """Gets Docker Container object from local Docker dameon based off of passed Service object.

    Specifically looks for a container with same name as passed Service object.
    """
    container: Optional[Container]
    if service is None:
        container = None
    else:
        try:
            container = docker.from_env().containers.get(service.container_name)
        except ContainerNotFoundError:
            container = None

    return container


def get_containers(services: Optional[List[Service]]) -> List[Container]:
    """Gets a list of containers based off of passed list."""
    if services is None:
        return []
    else:
        container_list = []
        for service in services:
            container = get_container(service)
            if container is not None:
                container_list.append(container)
        return container_list


def exec_in_container(container: Container, command: str) -> str:
    """Runs a command in passed docker container and returns command's output."""
    api_client = docker.APIClient()
    exec_id = api_client.exec_create(container.id, command)["Id"]
    return api_client.exec_start(exec_id).decode().strip()


def _filter_mounts(
    container: Container, expected_mount: BindMountInfo
) -> List[BindMountInfo]:
    mounts = get_mounts(container)
    assert mounts is not None, "mounts are None"
    return [mount for mount in mounts if mount == expected_mount]


def _filter_volumes(
    container: Container, expected_vol: NamedVolumeInfo
) -> List[NamedVolumeInfo]:
    volumes = get_volumes(container)
    assert volumes is not None, "volumes are None"
    filtered_volume = [volume for volume in volumes if volume == expected_vol]

    return filtered_volume


def confirm_named_volume_exists(
    container: Container, expected_vol: NamedVolumeInfo
) -> bool:
    """Helper method to assert that exected named volume exists on Docker container."""
    return len(_filter_volumes(container, expected_vol)) == 1


def confirm_named_volume_does_not_exist(
    container: Container, expected_vol: NamedVolumeInfo
) -> bool:
    """Helper method to assert that expected named volue does NOT exist on Docker container."""
    return len(_filter_volumes(container, expected_vol)) == 0


def confirm_mount_exists(container: Container, expected_mount: BindMountInfo) -> bool:
    """Helper method to assert that mount exists on Docker container."""
    return len(_filter_mounts(container, expected_mount)) == 1


def confirm_mount_does_not_exist(
    container: Container, expected_mount: BindMountInfo
) -> bool:
    """Helper method to assert that mount does NOT exist on Docker container."""
    return len(_filter_mounts(container, expected_mount)) == 0
