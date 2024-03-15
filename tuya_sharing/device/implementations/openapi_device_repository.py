"""device api."""
from __future__ import annotations
from typing import Any

from ...customerapi import CustomerApi
from ...customerlogging import logger
from ..function import DeviceFunction
from ..status_range import DeviceStatusRange
from ..customer_device import CustomerDevice
from ..abc import IDeviceRepository
from ..filter import Filter

class OpenAPIDeviceRepository(IDeviceRepository):
    def __init__(self, customer_api: CustomerApi):
        self.api = customer_api
        self.filter = Filter(10)

    def query_devices_by_home(self, home_id: str) -> list[CustomerDevice]:
        # 
        response = self.api.get(f"/v1.0/homes/{home_id}/devices", None)
        return self._query_devices(response)

    def query_devices_by_ids(self, ids: list) -> list[CustomerDevice]:
        response = self.api.get("/v2.0/cloud/thing/batch", {"device_ids": ",".join(ids)})
        return self._query_devices(response)

    def _query_devices(self, response) -> list[CustomerDevice]:
        _devices = []
        if response["success"]:
            for item in response["result"]:
                device = CustomerDevice(**item)
                status = {}
                for item_status in device.status:
                    if "code" in item_status and "value" in item_status:
                        code = item_status["code"]
                        value = item_status["value"]
                        status[code] = value
                device.status = status
                self.update_device_specification(device)
                self.update_device_strategy_info(device)
                _devices.append(device)
        return _devices

    def update_device_specification(self, device: CustomerDevice):
        device_id = device.id
        response = self.api.get(f"/v1.0/iot-03/devices/{device_id}/specification")
        if response.get("success"):
            result = response.get("result", {})
            function_map = {}
            for function in result["functions"]:
                code = function["code"]
                function_map[code] = DeviceFunction(**function)

            status_range = {}
            for status in result["status"]:
                code = status["code"]
                status_range[code] = DeviceStatusRange(**status)

            device.function = function_map
            device.status_range = status_range

    def update_device_strategy_info(self, device: CustomerDevice):
        device_id = device.id
        device.support_local = False
        device.local_strategy = {}
        # response = self.api.get(f"/v2.0/cloud/thing/{device_id}/shadow/properties")
        # response = self.api.get(f"/v1.0/m/life/devices/{device_id}/status")

        # TODO: See if we can expand to support local integrations


        logger.debug(
            f"device status strategy dev_id = {device_id} support_local = {device.support_local} local_strategy = {device.dp_id_map}")

    def send_commands(self, device_id: str, commands: list[dict[str, Any]]):
        if self.filter.call(device_id, commands):
            self.api.post(f"/v1.0/iot-03/devices/{device_id}/commands", None, {"commands": commands})

