import pytest
from unittest.mock import Mock
from ..order_tracker import OrderTracker

# --- Fixtures for Unit Tests ---

@pytest.fixture
def mock_storage():
    """
    Provides a mock storage object for tests.
    This mock will be configured to simulate various storage behaviors.
    """
    mock = Mock()
    # By default, mock get_order to return None (no order found)
    mock.get_order.return_value = None
    # By default, mock get_all_orders to return an empty dict
    mock.get_all_orders.return_value = {}
    return mock

@pytest.fixture
def order_tracker(mock_storage):
    """
    Provides an OrderTracker instance initialized with the mock_storage.
    """
    return OrderTracker(mock_storage)

def test_add_order_successfully(order_tracker, mock_storage):
    """Tests adding a new order with default 'pending' status."""
    order_tracker.add_order("ORD001", "Laptop", 1, "CUST001")

    mock_storage.save_order.assert_called_once_with(
        "ORD001",
        {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending",
        },
    )


def test_add_order_raises_error_if_exists(order_tracker, mock_storage):
    """Tests that adding an order with a duplicate ID raises a ValueError."""
    mock_storage.get_order.return_value = {"order_id": "ORD_EXISTING"}

    with pytest.raises(ValueError, match="Order with ID 'ORD_EXISTING' already exists."):
        order_tracker.add_order("ORD_EXISTING", "New Item", 1, "CUST001")


def test_add_order_raises_for_invalid_quantity(order_tracker):
    with pytest.raises(ValueError, match="quantity must be a positive integer."):
        order_tracker.add_order("ORD001", "Laptop", 0, "CUST001")


def test_get_order_by_id_existing(order_tracker, mock_storage):
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending",
    }

    result = order_tracker.get_order_by_id("ORD001")

    assert result["order_id"] == "ORD001"
    mock_storage.get_order.assert_called_once_with("ORD001")


def test_get_order_by_id_returns_none_for_missing(order_tracker, mock_storage):
    mock_storage.get_order.return_value = None

    result = order_tracker.get_order_by_id("UNKNOWN")

    assert result is None


def test_get_order_by_id_raises_for_empty_id(order_tracker):
    with pytest.raises(ValueError, match="order_id must be a non-empty string."):
        order_tracker.get_order_by_id("")


def test_update_order_status_success(order_tracker, mock_storage):
    mock_storage.get_order.return_value = {
        "order_id": "ORD001",
        "item_name": "Laptop",
        "quantity": 1,
        "customer_id": "CUST001",
        "status": "pending",
    }

    updated = order_tracker.update_order_status("ORD001", "shipped")

    assert updated["status"] == "shipped"
    mock_storage.save_order.assert_called_once_with(
        "ORD001",
        {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "shipped",
        },
    )


def test_update_order_status_raises_for_invalid_status(order_tracker, mock_storage):
    with pytest.raises(ValueError, match="new_status must be one of"):
        order_tracker.update_order_status("ORD001", "in_transit")

    mock_storage.get_order.assert_not_called()


def test_update_order_status_raises_for_missing_order(order_tracker, mock_storage):
    mock_storage.get_order.return_value = None

    with pytest.raises(ValueError, match="Order with ID 'ORD404' does not exist."):
        order_tracker.update_order_status("ORD404", "shipped")


def test_update_order_status_raises_for_empty_order_id(order_tracker):
    with pytest.raises(ValueError, match="order_id must be a non-empty string."):
        order_tracker.update_order_status("", "shipped")


def test_list_all_orders_returns_all(order_tracker, mock_storage):
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending",
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Mouse",
            "quantity": 2,
            "customer_id": "CUST002",
            "status": "shipped",
        },
    }

    results = order_tracker.list_all_orders()

    assert len(results) == 2
    assert {order["order_id"] for order in results} == {"ORD001", "ORD002"}


def test_list_all_orders_returns_empty_list(order_tracker, mock_storage):
    mock_storage.get_all_orders.return_value = {}

    assert order_tracker.list_all_orders() == []


def test_list_orders_by_status_returns_matching(order_tracker, mock_storage):
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending",
        },
        "ORD002": {
            "order_id": "ORD002",
            "item_name": "Mouse",
            "quantity": 2,
            "customer_id": "CUST002",
            "status": "shipped",
        },
    }

    pending_orders = order_tracker.list_orders_by_status("pending")

    assert len(pending_orders) == 1
    assert pending_orders[0]["order_id"] == "ORD001"


def test_list_orders_by_status_returns_empty_when_no_match(order_tracker, mock_storage):
    mock_storage.get_all_orders.return_value = {
        "ORD001": {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 1,
            "customer_id": "CUST001",
            "status": "pending",
        }
    }

    assert order_tracker.list_orders_by_status("cancelled") == []


def test_list_orders_by_status_raises_for_invalid_status(order_tracker):
    with pytest.raises(ValueError, match="status must be one of"):
        order_tracker.list_orders_by_status("unknown")
