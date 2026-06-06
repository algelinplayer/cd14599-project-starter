# Udatracker Starter Code

## Reflection

- I kept validation and business rules inside `OrderTracker` and made the Flask routes thin adapters. The trade-off is a little extra mapping logic in `app.py`, but this keeps the core behavior framework-agnostic, easier to unit test, and safer to evolve without route-level duplication.
- A key testing insight came from the failing red phase: status update and filtering edge cases quickly exposed missing validation paths. Writing targeted tests for invalid status, duplicate IDs, and blank IDs forced explicit error handling and prevented hidden assumptions in both unit and integration layers.
- If I continued this project, my next step would be adding a `DELETE /api/orders/<order_id>` endpoint with tests first, then introducing persistent storage (SQLite/PostgreSQL) behind the same storage interface so behavior stays stable while durability and real-world data consistency improve.

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/orders` | POST | Create a new order. |
| `/api/orders/<order_id>` | GET | Retrieve one order by ID. |
| `/api/orders/<order_id>/status` | PUT | Update order status. |
| `/api/orders` | GET | List orders. Supports `status` and `customer_id` query params. |
| `/api/orders/<order_id>` | DELETE | Delete an order by ID. |

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
