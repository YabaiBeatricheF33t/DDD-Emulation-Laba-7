from typing import Optional
from interfaces import OrderRepository, PaymentGateway
from domain.entities import Order
from domain.value_objects import Money


class PayOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_gateway: PaymentGateway
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> dict:
        # Load order
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return {"success": False, "error": "Order not found"}
        
        try:
            # Execute domain payment operation
            order.pay()
            
            # Call payment gateway
            payment_success = self.payment_gateway.charge(order_id, order.total_amount)
            
            if not payment_success:
                return {"success": False, "error": "Payment gateway failed"}
            
            # Save order
            self.order_repository.save(order)
            
            return {
                "success": True,
                "order_id": order_id,
                "amount": order.total_amount.amount,
                "currency": order.total_amount.currency
            }
            
        except ValueError as e:
            return {"success": False, "error": str(e)}