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

class APIGWDeviceRepository(IDeviceRepository):
    def __init__(self, customer_api: CustomerApi):
        self.api = customer_api
        self.filter = Filter(10)

    def query_devices_by_home(self, home_id: str) -> list[CustomerDevice]:
        response = self.api.get(f"/v1.0/m/life/ha/home/devices", {"homeId": home_id})
        return self._query_devices(response)

    def query_devices_by_ids(self, ids: list) -> list[CustomerDevice]:
        response = self.api.get("/v1.0/m/life/ha/devices/detail", {"devIds": ",".join(ids)})
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
        response = self.api.get(f"/v1.1/m/life/{device_id}/specifications")
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
        response = self.api.get(f"/v1.0/m/life/devices/{device_id}/status")
        support_local = True
        if response.get("success"):
            result = response.get("result", {})
            pid = result["productKey"]
            dp_id_map = {}
            for dp_status_relation in result["dpStatusRelationDTOS"]:
                if not dp_status_relation["supportLocal"]:
                    support_local = False
                    break
                # statusFormat valueDesc、valueType,enumMappingMap,pid
                dp_id_map[dp_status_relation["dpId"]] = {
                    "value_convert": dp_status_relation["valueConvert"],
                    "status_code": dp_status_relation["statusCode"],
                    "config_item": {
                        "statusFormat": dp_status_relation["statusFormat"],
                        "valueDesc": dp_status_relation["valueDesc"],
                        "valueType": dp_status_relation["valueType"],
                        "enumMappingMap": dp_status_relation["enumMappingMap"],
                        "pid": pid,
                    }
                }
            device.support_local = support_local
            if support_local:
                device.local_strategy = dp_id_map

            logger.debug(
                f"device status strategy dev_id = {device_id} support_local = {support_local} local_strategy = {dp_id_map}")

    def send_commands(self, device_id: str, commands: list[dict[str, Any]]):
        if self.filter.call(device_id, commands):
            self.api.post(f"/v1.1/m/thing/{device_id}/commands", None, {"commands": commands})


