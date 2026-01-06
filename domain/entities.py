from dataclasses import dataclass, field
from typing import List
from decimal import Decimal
from .value_objects import Money
from .enums import OrderStatus


@dataclass
class OrderLine:
    product_id: str
    product_name: str
    quantity: int
    unit_price: Money
    
    def total_price(self) -> Money:
        return Money(
            self.unit_price.amount * Decimal(self.quantity),
            self.unit_price.currency
        )


@dataclass
class Order:
    id: str
    customer_id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    _total_amount: Money = field(default_factory=lambda: Money(Decimal('0')))
    
    def __post_init__(self):
        self._calculate_total()
    
    def _calculate_total(self):
        if not self.lines:
            self._total_amount = Money(Decimal('0'))
            return
        
        total = Money(Decimal('0'))
        for line in self.lines:
            total = total + line.total_price()
        self._total_amount = total
    
    def add_line(self, line: OrderLine):
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify order after payment")
        self.lines.append(line)
        self._calculate_total()
    
    def remove_line(self, product_id: str):
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify order after payment")
        self.lines = [line for line in self.lines if line.product_id != product_id]
        self._calculate_total()
    
    def pay(self):
        if not self.lines:
            raise ValueError("Cannot pay empty order")
        
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        
        self.status = OrderStatus.PAID
    
    @property
    def total_amount(self) -> Money:
        return self._total_amount
    
    def is_empty(self) -> bool:
        return len(self.lines) == 0