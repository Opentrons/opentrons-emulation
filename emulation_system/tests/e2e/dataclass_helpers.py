"""Functions to assist with dataclass weirdness"""

import copy
from dataclasses import fields, is_dataclass
from typing import ClassVar, Dict, Protocol, Any


class IsDataclass(Protocol):
    """Determine from structural sub typing is an object is a dataclass."""
    __dataclass_fields__: ClassVar[Dict]

def __inner_convert_to_dict(obj):  # noqa: ANN001, ANN203
    """Method to handle converting dataclass into raw values.

    Base logic pulled from source code of dataclasses.asdict.
    Added handling for set objects. Removed handling for named tuples
    """
    if is_dataclass(obj):
        result = []
        for field in fields(obj):
            value = __inner_convert_to_dict(getattr(obj, field.name))
            result.append((field.name, value))
        return dict(result)
    elif isinstance(obj, (list, tuple)):
        return type(obj)(__inner_convert_to_dict(v) for v in obj)
    elif isinstance(obj, set):
        return {
            frozenset((k, v) for k, v in __inner_convert_to_dict(instance).items())
            for instance in obj
        }

    elif isinstance(obj, dict):
        return dict(
            (__inner_convert_to_dict(k), __inner_convert_to_dict(v))
            for k, v in obj.items()
        )
    else:
        return copy.deepcopy(obj)


def convert_to_dict(obj: IsDataclass) -> Dict[str, Any]:
    """Converts dataclass objects into raw values of dicts, list, sets, and tuples."""
    if not is_dataclass(obj):
        raise TypeError("Must pass dataclass type")
    return __inner_convert_to_dict(obj)
