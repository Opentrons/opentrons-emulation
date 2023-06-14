"""Common utilities for yaml operations."""

from yaml.dumper import Dumper


class OpentronsEmulationYamlDumper(Dumper):
    """Custom dumper to override default.

    Passed to yaml.dump module function

    Explanation of changes:
    - Remove `null` from outputted YAML file. Instead make it blank
    - Do not use YAML aliases
    """

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        self.add_representer(
            type(None),
            lambda dumper, value: dumper.represent_scalar("tag:yaml.org,2002:null", ""),
        )
        super().__init__(*args, **kwargs)

    # Don't know what type `data` is and I don't really care.
    # This class will never be used directly.
    # Also do not care about having a docstring.

    def ignore_aliases(self, data) -> bool:  # noqa: ANN001, D102
        return True
