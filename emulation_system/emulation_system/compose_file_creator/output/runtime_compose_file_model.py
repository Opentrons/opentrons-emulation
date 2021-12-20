"""Adds functions to generated compose_file_model."""
import os
from typing import Any

from yaml import dump as yaml_dump

from emulation_system.compose_file_creator.output.compose_file_model import (
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

    def to_compose_file(self, file_path: str) -> None:
        """Convert pydantic model to compose file at passed file_path."""
        yaml_content = self.to_yaml()
        file = open(file_path, "w")
        file.write(yaml_content)


if __name__ == "__main__":
    model = RuntimeComposeFileModel()
    service_1 = Service(image="hello-world", container_name="hello-world")
    model.services = {"hello-world": service_1}
    file_path = os.path.join(os.getcwd(), "../docker-compose.yml")
    print(model.to_yaml())  # type: ignore
    model.to_compose_file(file_path)  # type: ignore
