"""device api."""
from __future__ import annotations
from types import SimpleNamespace
from typing import Any


class DeviceFunction(SimpleNamespace):
    """device's function.

    Attributes:
        code(str): function's code
        desc(str): function's description
        name(str): function's name
        type(str): function's type, which may be Boolean, Integer, Enum, Json
        values(dict): function's value range
    """

    code: str
    desc: str
    name: str
    type: str
    values: dict[str, Any]

