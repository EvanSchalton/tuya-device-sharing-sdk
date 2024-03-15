from abc import ABC, abstractmethod
from ..customerapi import CustomerApi
from .smart_life_home import SmartLifeHome

class IHomeRepository(ABC):
    def __init__(self, customer_api: CustomerApi):
        self.api = customer_api

    @abstractmethod
    def query_homes(self) -> list[SmartLifeHome]:
        pass
