from abc import ABC, abstractmethod
from typing import Optional
from domain.entities import Order
from domain.value_objects import Money


class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def save(self, order: Order) -> None:
        pass


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, order_id: str, money: Money) -> bool:
        pass