"""Adds functions to generated compose_file_model."""
from typing import Any

import yaml

# Have to ignore attr-defined errors from mypy because we are calling type: ignore at
# the top of compose_file_model. This causes mypy to think that ComposeSpecification
# and Service do not exist when they actually do.
from emulation_system.compose_file_creator.output.compose_file_model import (  # type: ignore[attr-defined] # noqa: E501
    ComposeSpecification,
)


def represent_none(self, _):  # noqa: ANN001 ANN201
    """Override how yaml is formatted and instead of putting null, leave it blank."""
    return self.represent_scalar("tag:yaml.org,2002:null", "")


yaml.add_representer(type(None), represent_none)


class RuntimeComposeFileModel(ComposeSpecification):
    """Class to add functionality to generated ComposeSpecification model."""

    def __init__(self, **data: Any) -> None:
        """Initialize ComposeSpecification."""
        super().__init__(**data)

    def to_yaml(self) -> str:
        """Convert pydantic model to yaml."""
        return yaml.dump(self.dict(exclude_none=True), default_flow_style=False)
