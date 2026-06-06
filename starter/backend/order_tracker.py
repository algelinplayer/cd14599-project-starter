# This module contains the OrderTracker class, which encapsulates the core
# business logic for managing orders.

class OrderTracker:
    """
    Manages customer orders, providing functionalities to add, update,
    and retrieve order information.
    """
    def __init__(self, storage):
        required_methods = ['save_order', 'get_order', 'get_all_orders', 'delete_order']
        for method in required_methods:
            if not hasattr(storage, method) or not callable(getattr(storage, method)):
                raise TypeError(f"Storage object must implement a callable '{method}' method.")
        self.storage = storage
        self.valid_statuses = {"pending", "processing", "shipped", "delivered", "cancelled"}

    def _validate_non_empty_string(self, value: str, field_name: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} must be a non-empty string.")

    def _validate_status(self, status: str, field_name: str = "status"):
        if status not in self.valid_statuses:
            allowed = ", ".join(sorted(self.valid_statuses))
            raise ValueError(f"{field_name} must be one of: {allowed}.")

    def add_order(self, order_id: str, item_name: str, quantity: int, customer_id: str, status: str = "pending"):
        self._validate_non_empty_string(order_id, "order_id")
        self._validate_non_empty_string(item_name, "item_name")
        self._validate_non_empty_string(customer_id, "customer_id")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("quantity must be a positive integer.")
        self._validate_status(status, "status")

        if self.storage.get_order(order_id):
            raise ValueError(f"Order with ID '{order_id}' already exists.")

        order = {
            "order_id": order_id,
            "item_name": item_name,
            "quantity": quantity,
            "customer_id": customer_id,
            "status": status,
        }
        self.storage.save_order(order_id, order)
        return order

    def get_order_by_id(self, order_id: str):
        self._validate_non_empty_string(order_id, "order_id")
        return self.storage.get_order(order_id)

    def update_order_status(self, order_id: str, new_status: str):
        self._validate_non_empty_string(order_id, "order_id")
        self._validate_status(new_status, "new_status")

        order = self.storage.get_order(order_id)
        if not order:
            raise ValueError(f"Order with ID '{order_id}' does not exist.")

        updated_order = order.copy()
        updated_order["status"] = new_status
        self.storage.save_order(order_id, updated_order)
        return updated_order

    def list_all_orders(self):
        all_orders = self.storage.get_all_orders()
        return list(all_orders.values())

    def list_orders_by_status(self, status: str):
        self._validate_status(status, "status")
        all_orders = self.list_all_orders()
        return [order for order in all_orders if order.get("status") == status]

    def delete_order_by_id(self, order_id: str):
        self._validate_non_empty_string(order_id, "order_id")

        order = self.storage.get_order(order_id)
        if not order:
            raise ValueError(f"Order with ID '{order_id}' does not exist.")

        self.storage.delete_order(order_id)
        return order
