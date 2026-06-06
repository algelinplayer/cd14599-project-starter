# Udatracker User Stories and Acceptance Criteria

## US-01: Create a New Order
**User Story:** As a customer, I want to place a new order so that it can be tracked.

**Acceptance Criteria:**
- `add_order` stores order fields: `order_id`, `item_name`, `quantity`, `customer_id`, `status`.
- Default `status` is `pending` when omitted.
- Duplicate `order_id` is rejected with a clear validation error.
- Invalid order input is rejected (at least one invalid case covered by tests).
- API: `POST /api/orders` returns `201` with created order JSON on success.

## US-02: Retrieve an Order by ID
**User Story:** As a customer, I want to retrieve an order by ID so that I can check its details.

**Acceptance Criteria:**
- `get_order_by_id` returns the full order for an existing ID.
- Returns `None` for non-existent order IDs.
- Empty or invalid ID is handled by validation/error behavior.
- API: `GET /api/orders/<order_id>` returns `200` for existing order and `404` when missing.

## US-03: Update Order Status
**User Story:** As a customer or operator, I want to update an order status so that order progress is accurate.

**Acceptance Criteria:**
- `update_order_status` updates status for an existing order.
- Allowed statuses: `pending`, `processing`, `shipped`, `delivered`, `cancelled`.
- Invalid status is rejected.
- Non-existent order update is rejected.
- Empty order ID is rejected.
- API: `PUT /api/orders/<order_id>/status` returns `200` with updated JSON on success.

## US-04: List All Orders
**User Story:** As a user, I want to view all orders so that I can review all current records.

**Acceptance Criteria:**
- `list_all_orders` returns a list of all orders.
- Returns an empty list when storage is empty.
- API: `GET /api/orders` returns `200` and all created orders.

## US-05: Filter Orders by Status
**User Story:** As a user, I want to filter orders by status so that I can focus on a specific workflow stage.

**Acceptance Criteria:**
- `list_orders_by_status` returns only orders matching the requested status.
- Returns empty list when there are no matches.
- Empty or invalid status is rejected.
- API: `GET /api/orders?status=<status>` returns `200` with matching orders.

## US-06: Filter Orders by Customer
**User Story:** As an operator, I want to filter orders by customer ID so I can review one customer’s orders quickly.

**Acceptance Criteria:**
- API: `GET /api/orders?customer_id=<customer_id>` returns only matching customer orders.
- API supports combined filtering with status (e.g., `?customer_id=C123&status=pending`).
- Empty customer filter is rejected with a validation error and a JSON error response.

## US-07: Delete an Order
**User Story:** As an operator, I want to delete an order so incorrect or cancelled records can be removed.

**Acceptance Criteria:**
- `delete_order_by_id` deletes an existing order and returns deleted order data.
- Deleting a non-existent order returns a not-found style error.
- Empty order ID is rejected.
- API: `DELETE /api/orders/<order_id>` returns `204 No Content` on success.

## US-08: Consistent API Error Responses
**User Story:** As an API consumer, I want consistent error JSON payloads so client-side handling is predictable.

**Acceptance Criteria:**
- Validation failures return `400` with `{"error": "message"}`.
- Missing resources return `404` with `{"error": "message"}`.
- Conflict cases (duplicate order ID) return `409` with `{"error": "message"}`.
- Error response formatting is centralized via Flask error handlers.

---

## Progress Tracking
- [x] Step 1 completed: Project overview and rubric reviewed.
- [x] Step 2 completed: Tests expanded and red/green cycle executed.
- [x] Step 3 completed: Backend logic implemented and covered by unit tests.
- [x] Step 4 completed: API implemented with integration tests.
- [x] Step 5 completed: Reflection added to `starter/README.md`.
- [x] Post-review enhancements completed: consistent error handling, customer filtering, delete endpoint, API docs, and Dockerfile.