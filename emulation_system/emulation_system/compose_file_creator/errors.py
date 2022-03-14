"""One-stop shop for all errors."""

from typing import List, Set

from emulation_system.compose_file_creator.settings.config_file_settings import Hardware


class MountError(Exception):
    """Base mount exception."""

    ...


class NoMountsDefinedError(MountError):
    """Exception thrown when you try to load a mount and none are defined."""

    def __init__(self) -> None:
        super().__init__("You have no mounts defined.")


class MountNotFoundError(MountError):
    """Exception thrown when mount of a certain name is not found."""

    def __init__(self, name: str) -> None:
        super().__init__(f'Mount named "{name}" not found.')


class EmulationLevelNotSupportedError(Exception):
    """Exception thrown when emulation level is not supported."""

    def __init__(self, emulation_level: str, hardware: str) -> None:
        super().__init__(
            f'Emulation level, "{emulation_level}" not supported for "{hardware}"'
        )


class LocalSourceDoesNotExistError(Exception):
    """Exception thrown when local source-location does not exist."""

    def __init__(self, path: str) -> None:
        super().__init__(f'"{path}" is not a valid directory path')


class InvalidRemoteSourceError(Exception):
    """Exception thrown when remote source is not valid."""

    def __init__(self, value: str) -> None:
        super().__init__(
            f'"{value}" is not valid. Must either be a valid commit sha, or the '
            f'value "latest"'
        )


class DuplicateHardwareNameError(Exception):
    """Exception thrown when there is hardware with duplicate names."""

    def __init__(self, duplicate_names: Set[str]) -> None:
        super().__init__(
            "The following container names are duplicated in the configuration file: "
            f"{', '.join(duplicate_names)}"
        )


class ImageNotDefinedError(Exception):
    """Exception thrown when there is no image defined for specified emulation level/source type."""  # noqa: E501

    def __init__(self, emulation_level: str, source_type: str, hardware: str) -> None:
        super().__init__(
            f'Image with emulation level of "{emulation_level}" and source type '
            f'"{source_type}" does not exist for {hardware}'
        )


class IncorrectHardwareError(Exception):
    """Exception thrown when incorrect hardware is specified."""

    def __init__(
        self, specifed_hardware: Hardware, expected_hardware: Hardware
    ) -> None:
        super().__init__(
            f"Incorrect hardware specifed: {specifed_hardware}. "
            f"Expected: {expected_hardware}"
        )


class HardwareDoesNotExistError(Exception):
    """Exception thrown when hardware does not exist."""

    def __init__(self, specified_hardware: Hardware) -> None:
        super().__init__(f"{specified_hardware} not defined.")


class RepoDoesNotExistError(Exception):
    """Exception thrown when repo does not exist."""

    def __init__(self, repo_name: str) -> None:
        super().__init__(f'Repo "{repo_name}" does not exist.')


class ServiceDoesNotExistError(Exception):
    """Exception thrown when Robot Server does not exist."""

    def __init__(self, service_name: str) -> None:
        super().__init__(
            f"You do not have a {service_name} in your generated configuration."
        )


class NotRemoteOnlyError(Exception):
    """Exception thrown when not any robot or module is not of remote source-type."""

    def __init__(self) -> None:
        super().__init__(
            'Not all source-type parameters for passed system are "remote".'
        )


class InvalidFilterError(Exception):
    """Exception thrown when Robot Server does not exist."""

    def __init__(self, filter_name: str, valid_filters: List[str]) -> None:
        valid_names = "\n\t".join(valid_filters)
        valid_not_names = "\n\tnot-".join(valid_filters)
        super().__init__(
            f'\n\nFilter name "{filter_name}" is invalid.\n'
            f"Valid filter names are \n\t{valid_names}\n\n\tnot-{valid_not_names}\n"
        )
