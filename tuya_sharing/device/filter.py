"""device api."""
from __future__ import annotations
import time
from ..customerlogging import logger


class Filter:
    def __init__(self, time: int):
        self.last_call_time = {}
        self.time_limit = time
        self.last_clean_time = 0

    def clean_expired_keys(self):
        current_time = time.time()
        if current_time - self.last_clean_time >= 10:
            expired_keys = [key for key, (_, last_time) in self.last_call_time.items() if
                            current_time - last_time >= 10]
            for key in expired_keys:
                del self.last_call_time[key]
            self.last_clean_time = current_time

    def call(self, dev_id, param) -> bool:
        self.clean_expired_keys()

        current_time = time.time()
        if dev_id in self.last_call_time:
            last_param, last_time = self.last_call_time[dev_id]
            if param != last_param or current_time - last_time >= self.time_limit:
                self.last_call_time[dev_id] = (param, current_time)
                logger.debug(f"filter receive one dev_id = {dev_id} param = {param}")
                return True
            else:
                logger.debug(f"filter receive two dev_id = {dev_id} param = {param}")
                return False
        else:
            self.last_call_time[dev_id] = (param, current_time)
            logger.debug(f"filter receive three dev_id = {dev_id} param = {param}")
            return True
