from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < Decimal('0'):
            raise ValueError("Money amount cannot be negative")
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"