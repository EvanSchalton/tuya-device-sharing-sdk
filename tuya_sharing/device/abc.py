"""device api."""
from __future__ import annotations
from abc import ABC
from typing import Any
from .customer_device import CustomerDevice

class IDeviceRepository(ABC):

    def query_devices_by_home(self, home_id: str) -> list[CustomerDevice]:
        pass

    def query_devices_by_ids(self, ids: list) -> list[CustomerDevice]:
        pass

    def _query_devices(self, response) -> list[CustomerDevice]:
        pass

    def update_device_specification(self, device: CustomerDevice):
        pass

    def update_device_strategy_info(self, device: CustomerDevice):
        pass

    def send_commands(self, device_id: str, commands: list[dict[str, Any]]):
        pass



