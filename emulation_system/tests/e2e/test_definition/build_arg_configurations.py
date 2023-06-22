"""Class representing where source code was pulled from for given container."""

from enum import Enum, auto
from typing import Dict

from docker.models.containers import Container  # type: ignore[import]

from emulation_system import git_interaction
from emulation_system.compose_file_creator.config_file_settings import (
    OpentronsRepository,
)


class BuildArgConfigurations(Enum):
    """Represents where source code was pulled from."""

    NO_BUILD_ARGS = auto()
    LATEST_BUILD_ARGS = auto()
    REF_BUILD_ARGS = auto()

    @staticmethod
    def _convert_env_list_to_dict(container: Container) -> Dict[str, str]:
        """List of env vars are key value pairs separated by an equals sign."""
        return dict(
            [env_val.split("=", 1) for env_val in container.attrs["Config"]["Env"]]
        )

    @classmethod
    def parse_build_args(
        cls, container: Container, repo: OpentronsRepository
    ) -> "BuildArgConfigurations":
        """Parses out source code build args from env vars.

        Having to pass build args as env variables so they can be seen
        by the Docker SDK. Build args are not passed to a running container.
        """
        build_arg_name = repo.build_arg_name
        head_ref = repo.default_branch
        if container is None:
            return cls.NO_BUILD_ARGS

        monorepo_env_dict = cls._convert_env_list_to_dict(container)
        if build_arg_name not in monorepo_env_dict.keys():
            return cls.NO_BUILD_ARGS

        build_arg_state: BuildArgConfigurations
        build_arg_val = monorepo_env_dict[build_arg_name]

        if build_arg_val.endswith(head_ref):
            build_arg_state = cls.LATEST_BUILD_ARGS
        elif git_interaction.check_if_ref_exists(repo.OWNER, repo.value, build_arg_val):
            build_arg_state = cls.REF_BUILD_ARGS
        else:
            raise ValueError("Build arg did not match anything.")

        return build_arg_state
