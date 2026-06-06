# Udatracker Starter Code

## Reflection

- I kept validation and business rules inside `OrderTracker` and made the Flask routes thin adapters. The trade-off is a little extra mapping logic in `app.py`, but this keeps the core behavior framework-agnostic, easier to unit test, and safer to evolve without route-level duplication.
- A key testing insight came from the failing red phase: status update and filtering edge cases quickly exposed missing validation paths. Writing targeted tests for invalid status, duplicate IDs, and blank IDs forced explicit error handling and prevented hidden assumptions in both unit and integration layers.
- If I continued this project, my next step would be adding a `DELETE /api/orders/<order_id>` endpoint with tests first, then introducing persistent storage (SQLite/PostgreSQL) behind the same storage interface so behavior stays stable while durability and real-world data consistency improve.

## API Reference

The full OpenAPI specification is also available at `starter/openapi.yaml`.

```yaml
openapi: 3.0.3
info:
  title: Udatracker Order API
  version: 1.0.0
paths:
  /api/orders:
    get:
      summary: List orders
      parameters:
        - in: query
          name: status
          schema:
            type: string
            enum: [pending, processing, shipped, delivered, cancelled]
        - in: query
          name: customer_id
          schema:
            type: string
      responses:
        "200":
          description: Orders returned
        "400":
          description: Validation error
    post:
      summary: Create order
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [order_id, item_name, quantity, customer_id]
              properties:
                order_id: { type: string }
                item_name: { type: string }
                quantity: { type: integer, minimum: 1 }
                customer_id: { type: string }
                status:
                  type: string
                  enum: [pending, processing, shipped, delivered, cancelled]
      responses:
        "201":
          description: Order created
        "400":
          description: Validation error
        "409":
          description: Duplicate order ID
  /api/orders/{order_id}:
    get:
      summary: Get order by ID
      parameters:
        - in: path
          name: order_id
          required: true
          schema:
            type: string
      responses:
        "200":
          description: Order found
        "404":
          description: Order not found
    delete:
      summary: Delete order by ID
      parameters:
        - in: path
          name: order_id
          required: true
          schema:
            type: string
      responses:
        "204":
          description: Order deleted
        "404":
          description: Order not found
  /api/orders/{order_id}/status:
    put:
      summary: Update order status
      parameters:
        - in: path
          name: order_id
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [new_status]
              properties:
                new_status:
                  type: string
                  enum: [pending, processing, shipped, delivered, cancelled]
      responses:
        "200":
          description: Status updated
        "400":
          description: Validation error
        "404":
          description: Order not found
```

### Sample curl commands

```bash
curl -X POST http://127.0.0.1:5000/api/orders -H "Content-Type: application/json" -d "{\"order_id\":\"DOC001\",\"item_name\":\"Keyboard\",\"quantity\":1,\"customer_id\":\"C100\"}"
curl http://127.0.0.1:5000/api/orders?status=pending&customer_id=C100
curl -X PUT http://127.0.0.1:5000/api/orders/DOC001/status -H "Content-Type: application/json" -d "{\"new_status\":\"shipped\"}"
curl -X DELETE http://127.0.0.1:5000/api/orders/DOC001
```

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── in_memory_storage.py
│   ├── order_tracker.py
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
│       ├── test_api.py
│       └── test_order_tracker.py
├── frontend
│   ├── css
│   │   └── style.css
│   ├── index.html
│   └── js
│       └── script.js
├── pytest.ini
└── README.md
```
