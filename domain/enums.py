from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"