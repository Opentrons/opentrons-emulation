"""Function useful to multiple service creation modules."""
from typing import List

def to_kebab(string: str) -> str:
    """Converts snake case formatted string to kebab case."""
    return string.replace("_", "-")
