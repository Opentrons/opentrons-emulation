"""Adds functions to generated compose_file_model."""
import os
from typing import Any

from yaml import dump as yaml_dump

# Have to ignore attr-defined errors from mypy because we are calling type: ignore at
# the top of compose_file_model. This causes mypy to think that ComposeSpecification
# and Service do not exist when they actually do.
from emulation_system.compose_file_creator.output.compose_file_model import (  # type: ignore[attr-defined] # noqa: E501
    ComposeSpecification,
    Service,
)


class RuntimeComposeFileModel(ComposeSpecification):
    """Class to add functionality to generated ComposeSpecification model."""

    def __init__(self, **data: Any) -> None:
        """Initialize ComposeSpecification."""
        super().__init__(**data)

    def to_yaml(self) -> str:
        """Convert pydantic model to yaml."""
        return yaml_dump(self.dict(exclude_none=True), default_flow_style=False)


if __name__ == "__main__":
    model = RuntimeComposeFileModel()
    service_1 = Service(image="hello-world", container_name="hello-world")
    model.services = {"hello-world": service_1}
    file_path = os.path.join(os.getcwd(), "../docker-compose.yml")
    print(model.to_yaml())  # type: ignore
    model.to_compose_file(file_path)  # type: ignore
