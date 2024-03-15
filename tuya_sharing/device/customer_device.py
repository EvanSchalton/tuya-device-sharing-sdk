"""device api."""
from __future__ import annotations
from types import SimpleNamespace
from typing import Any, Optional

from .function import DeviceFunction
from .status_range import DeviceStatusRange

class CustomerDevice(SimpleNamespace):
    """Customer Device.

    Attributes:
          id: Device id
          name: Device name
          local_key: Key
          category: Product category
          product_id: Product ID
          product_name: Product name
          sub: Determine whether it is a sub-device, true-> yes; false-> no
          uuid: The unique device identifier
          asset_id: asset id of the device
          online: Online status of the device
          icon: Device icon
          ip: Device IP
          time_zone: device time zone
          active_time: The last pairing time of the device
          create_time: The first network pairing time of the device
          update_time: The update time of device status

          status: Status set of the device
          function: Instruction set of the device
          status_range: Status value range set of the device
    """

    id: str
    name: str
    local_key: str
    category: str
    product_id: str
    product_name: str
    sub: bool
    uuid: str
    asset_id: str
    online: bool
    icon: str
    ip: str
    time_zone: str
    active_time: int
    create_time: int
    update_time: int
    set_up: Optional[bool] = False
    support_local: Optional[bool] = False
    local_strategy: dict[int, dict[str, Any]] = {}

    status: dict[str, Any] = {}
    function: dict[str, DeviceFunction] = {}
    status_range: dict[str, DeviceStatusRange] = {}

    def __eq__(self, other):
        """If devices are the same one."""
        return self.id == other.id

