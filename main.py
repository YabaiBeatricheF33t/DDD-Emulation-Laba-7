from decimal import Decimal
from domain.entities import Order, OrderLine
from domain.value_objects import Money
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase


def main():
    # Create infrastructure
    repository = InMemoryOrderRepository()
    payment_gateway = FakePaymentGateway()
    
    # Create order
    order = Order(id="order-123", customer_id="customer-456")
    order.add_line(OrderLine(
        product_id="prod-1",
        product_name="Laptop",
        quantity=1,
        unit_price=Money(Decimal('999.99'))
    ))
    order.add_line(OrderLine(
        product_id="prod-2",
        product_name="Mouse",
        quantity=2,
        unit_price=Money(Decimal('25.50'))
    ))
    
    # Save order
    repository.save(order)
    
    # Create use case
    use_case = PayOrderUseCase(repository, payment_gateway)
    
    # Execute payment
    result = use_case.execute("order-123")
    
    print("Payment result:", result)
    print("Order total:", order.total_amount)
    print("Order status:", order.status.value)


if __name__ == "__main__":
    main()