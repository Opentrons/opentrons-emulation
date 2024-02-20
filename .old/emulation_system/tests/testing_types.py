"""All testing types should be placed here."""

from typing import Dict, Literal

ModuleDeclaration = Dict[
    Literal[
        "heater-shaker-module",
        "thermocycler-module",
        "temperature-module",
        "magnetic-module",
    ],
    int,
]
