# Udatracker Starter Code

## Reflection

- I kept validation and business rules inside `OrderTracker` and made the Flask routes thin adapters. The trade-off is a little extra mapping logic in `app.py`, but this keeps the core behavior framework-agnostic, easier to unit test, and safer to evolve without route-level duplication.
- A key testing insight came from the failing red phase: status update and filtering edge cases quickly exposed missing validation paths. Writing targeted tests for invalid status, duplicate IDs, and blank IDs forced explicit error handling and prevented hidden assumptions in both unit and integration layers.
- If I continued this project, my next step would be adding a `DELETE /api/orders/<order_id>` endpoint with tests first, then introducing persistent storage (SQLite/PostgreSQL) behind the same storage interface so behavior stays stable while durability and real-world data consistency improve.

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
