from typing import Optional, Dict
from interfaces import OrderRepository
from domain.entities import Order


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def save(self, order: Order) -> None:
        self._orders[order.id] = order