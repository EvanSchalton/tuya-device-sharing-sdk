from __future__ import annotations
from typing import List
from ...customerapi import CustomerApi
from ..smart_life_home import SmartLifeHome
from ..abc import IHomeRepository

class OpenAPIHomeRepository(IHomeRepository):
    def __init__(self, customer_api: CustomerApi):
        self.api = customer_api

    def query_homes(self) -> list[SmartLifeHome]:
        # list spaces: https://openapi.tuyaus.com/v2.0/cloud/space/child?only_sub=true
        # {
        #   "result": {
        #     "data": [
        #       <home-id>          # <--- this is the home id
        #     ],
        #     "page_size": 200
        #   },
        #   "success": true,
        #   "t": ....,
        #   "tid": "..."
        # }

        # get the home owner: "https://openapi.tuyaus.com/v1.0/homes/{home_id}/members"
        # {
        # "result": [
        #     {
        #     "admin": true,
        #     "avatar": "",
        #     "country_code": "1",
        #     "member_account": "redacted-email",
        #     "name": "navenine",
        #     "owner": true,
        #     "uid": "<user_id>" # <--- this is the user id
        #     }
        # ],
        # "success": true,
        # "t": 1710541949347,
        # "tid": "e8218fa5e31b11eea9b80abc11d96f3d"
        # }

        response = self.api.get(f"/v2.0/cloud/space/child?only_sub=true")

        home_ids = response.get("result", {}).get("data", [])
        _homes: List[SmartLifeHome] = []
        for home_id in home_ids:
            self.api.get(f"/v1.0/homes/{home_id}/members")

            if response.get("success", False):
                for user_info in response.get("result", []):
                    if user_info.get("owner", False):
                        _homes.append(SmartLifeHome(str(user_info["uid"]), home_id))
        return _homes
