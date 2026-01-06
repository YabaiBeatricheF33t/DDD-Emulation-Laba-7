from interfaces import PaymentGateway
from domain.value_objects import Money


class FakePaymentGateway(PaymentGateway):
    def charge(self, order_id: str, money: Money) -> bool:
        # Always returns success for testing
        print(f"Charging {money} for order {order_id}")
        return True