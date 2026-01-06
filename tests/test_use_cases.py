import unittest
import sys
import os

# Добавляем корень проекта в Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, project_root)

from decimal import Decimal
from domain.entities import Order, OrderLine
from domain.value_objects import Money
from domain.enums import OrderStatus
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway
from application.use_cases import PayOrderUseCase

class TestPayOrderUseCase(unittest.TestCase):
    def setUp(self):
        self.repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.repository, self.payment_gateway)
    
    def create_sample_order(self) -> Order:
        order = Order(id="order-1", customer_id="customer-1")
        order.add_line(OrderLine(
            product_id="prod-1",
            product_name="Product 1",
            quantity=2,
            unit_price=Money(Decimal('10.50'))
        ))
        order.add_line(OrderLine(
            product_id="prod-2",
            product_name="Product 2",
            quantity=1,
            unit_price=Money(Decimal('5.00'))
        ))
        return order
    
    def test_successful_payment(self):
        # Arrange
        order = self.create_sample_order()
        self.repository.save(order)
        
        # Act
        result = self.use_case.execute("order-1")
        
        # Assert
        self.assertTrue(result["success"])
        self.assertEqual(result["order_id"], "order-1")
        self.assertEqual(result["amount"], Decimal('26.00'))  # 2*10.50 + 5.00 = 26.00
        
        # Check that order was saved with correct status
        saved_order = self.repository.get_by_id("order-1")
        self.assertEqual(saved_order.status, OrderStatus.PAID)
    
    def test_payment_empty_order(self):
        # Arrange
        order = Order(id="order-2", customer_id="customer-1")
        self.repository.save(order)
        
        # Act
        result = self.use_case.execute("order-2")
        
        # Assert
        self.assertFalse(result["success"])
        self.assertIn("Cannot pay empty order", result["error"])
    
    def test_double_payment(self):
        # Arrange
        order = self.create_sample_order()
        order.pay()  # First payment
        self.repository.save(order)
        
        # Act
        result = self.use_case.execute("order-1")
        
        # Assert
        self.assertFalse(result["success"])
        self.assertIn("Order already paid", result["error"])
    
    def test_cannot_modify_after_payment(self):
        # Arrange
        order = self.create_sample_order()
        order.pay()
        
        # Act & Assert
        with self.assertRaises(ValueError) as context:
            order.add_line(OrderLine(
                product_id="prod-3",
                product_name="Product 3",
                quantity=1,
                unit_price=Money(Decimal('15.00'))
            ))
        
        self.assertIn("Cannot modify order after payment", str(context.exception))
    
    def test_correct_total_calculation(self):
        # Arrange
        order = self.create_sample_order()
        
        # Assert
        self.assertEqual(order.total_amount.amount, Decimal('26.00'))
        
        # Add another product
        order.add_line(OrderLine(
            product_id="prod-3",
            product_name="Product 3",
            quantity=3,
            unit_price=Money(Decimal('7.00'))
        ))
        
        # 26.00 + 3*7.00 = 47.00
        self.assertEqual(order.total_amount.amount, Decimal('47.00'))
    
    def test_order_not_found(self):
        # Act
        result = self.use_case.execute("non-existent-order")
        
        # Assert
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Order not found")


if __name__ == '__main__':
    unittest.main()