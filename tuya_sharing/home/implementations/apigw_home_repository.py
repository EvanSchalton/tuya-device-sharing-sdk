from __future__ import annotations

from ...customerapi import CustomerApi
from ..smart_life_home import SmartLifeHome
from ..abc import IHomeRepository

class APIGWHomeRepository(IHomeRepository):
    def __init__(self, customer_api: CustomerApi):
        self.api = customer_api

    def query_homes(self) -> list[SmartLifeHome]:
        response = self.api.get(f"/v1.0/m/life/users/homes")

        if response.get("success", False):
            _homes = []
            for home in response["result"]:
                _home = SmartLifeHome(str(home["ownerId"]), home["name"])
                _homes.append(_home)
            return _homes

        return []
