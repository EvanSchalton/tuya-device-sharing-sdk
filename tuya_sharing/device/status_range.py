"""device api."""
from __future__ import annotations
from types import SimpleNamespace

class DeviceStatusRange(SimpleNamespace):
    """device's status range.

    Attributes:
        code(str): status's code
        type(str): status's type, which may be Boolean, Integer, Enum, Json
        values(dict): status's value range
    """

    code: str
    type: str
    values: str

