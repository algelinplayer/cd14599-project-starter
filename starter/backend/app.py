from flask import Flask, request, jsonify, send_from_directory
from backend.order_tracker import OrderTracker
from backend.in_memory_storage import InMemoryStorage


class ApiError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


app = Flask(__name__, static_folder='../frontend')
in_memory_storage = InMemoryStorage()
order_tracker = OrderTracker(in_memory_storage)


@app.errorhandler(ApiError)
def handle_api_error(error):
    return jsonify({'error': error.message}), error.status_code


@app.errorhandler(ValueError)
def handle_value_error(error):
    return jsonify({'error': str(error)}), 400

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/orders', methods=['POST'])
def add_order_api():
    data = request.get_json(silent=True) or {}
    try:
        order = order_tracker.add_order(
            data.get('order_id'),
            data.get('item_name'),
            data.get('quantity'),
            data.get('customer_id'),
            data.get('status', 'pending'),
        )
    except ValueError as exc:
        if 'already exists' in str(exc):
            raise ApiError(str(exc), 409) from exc
        raise
    return jsonify(order), 201

@app.route('/api/orders/<string:order_id>', methods=['GET'])
def get_order_api(order_id):
    order = order_tracker.get_order_by_id(order_id)

    if not order:
        raise ApiError('Order not found', 404)
    return jsonify(order), 200

@app.route('/api/orders/<string:order_id>/status', methods=['PUT'])
def update_order_status_api(order_id):
    data = request.get_json(silent=True) or {}
    try:
        updated_order = order_tracker.update_order_status(order_id, data.get('new_status'))
        return jsonify(updated_order), 200
    except ValueError as exc:
        status_code = 404 if 'does not exist' in str(exc) else 400
        return jsonify({'error': str(exc)}), status_code

@app.route('/api/orders', methods=['GET'])
def list_orders_api():
    status_filter = request.args.get('status')
    try:
        if status_filter is None:
            orders = order_tracker.list_all_orders()
        else:
            orders = order_tracker.list_orders_by_status(status_filter)
        return jsonify(orders), 200
    except ValueError as exc:
        return jsonify({'error': str(exc)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
