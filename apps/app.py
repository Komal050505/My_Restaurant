from flask import Flask, request, jsonify
from flask_cors import CORS
from logging_package.logging_module import log
from apps.constants import MENU, TABLES

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    """
    Home endpoint to welcome users to the restaurant.
    Logs the access and returns a welcome message.
    """
    log.info("Home endpoint accessed")
    return "Welcome to KOMAL'S Restaurant!"


@app.route('/menu', methods=['GET'])
def get_menu():
    """
    Endpoint to get the restaurant menu.
    Logs the action and returns the menu.
    Handles exceptions and logs errors.
    """

    try:
        return jsonify(MENU)
    except Exception as e:
        log.error(f"Error fetching menu: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


@app.route('/table/<int:table_id>/order', methods=['GET'])
def get_table_orders(table_id):
    """
    Endpoint to get orders for a specific table.
    Logs the action, checks if the table exists, and returns the orders.
    Handles exceptions and logs errors.
    """
    try:
        if table_id in TABLES:
            log.info(f"Fetching orders for Table {table_id} started")
            orders = TABLES[table_id]["orders"]
            return jsonify(orders)
        else:
            log.warning(f"Table {table_id} not found")
            return jsonify({"error": "Table not found"}), 404
    except Exception as e:
        log.error(f"Error fetching orders for Table {table_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Fetching orders for Table {table_id} ended")


@app.route('/table/<int:table_id>/order', methods=['POST'])
def create_table_order(table_id):
    """
    Endpoint to create an order for a specific table.
    Logs the action, checks if the table exists, and creates the order.
    Handles exceptions and logs errors.
    """
    try:
        if table_id in TABLES:
            log.info(f"Creating order for Table {table_id} started")
            new_order = request.json
            order_id = len(TABLES[table_id]["orders"]) + 1
            TABLES[table_id]["orders"][order_id] = new_order
            log.info(f"Order created for Table {table_id}: {new_order}")
            return jsonify({"order_id": order_id, "status": "Order received"}), 201
        else:
            log.warning(f"Table {table_id} not found")
            return jsonify({"error": "Table not found"}), 404
    except Exception as e:
        log.error(f"Error creating order for Table {table_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Creating order for Table {table_id} ended")


@app.route('/table/<int:table_id>/order/<int:order_id>', methods=['GET'])
def get_table_order(table_id, order_id):
    """
    Endpoint to get a specific order for a specific table.
    Logs the action, checks if the table and order exist, and returns the order.
    Handles exceptions and logs errors.
    """
    try:
        if table_id in TABLES and order_id in TABLES[table_id]["orders"]:
            log.info(f"Fetching order {order_id} for Table {table_id} started")
            order = TABLES[table_id]["orders"][order_id]
            return jsonify(order)
        else:
            log.warning(f"Order {order_id} not found for Table {table_id}")
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        log.error(f"Error fetching order {order_id} for Table {table_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Fetching order {order_id} for Table {table_id} ended")


@app.route('/table/<int:table_id>/order/<int:order_id>', methods=['PUT'])
def update_table_order(table_id, order_id):
    """
    Endpoint to update a specific order for a specific table.
    Logs the action, checks if the table and order exist, and updates the order.
    Handles exceptions and logs errors.
    """
    try:
        if table_id in TABLES and order_id in TABLES[table_id]["orders"]:
            log.info(f"Updating order {order_id} for Table {table_id} started")
            updated_order = request.json
            TABLES[table_id]["orders"][order_id].update(updated_order)
            log.info(f"Order {order_id} updated for Table {table_id}: {updated_order}")
            return jsonify({"order_id": order_id, "status": "Order updated"})
        else:
            log.warning(f"Order {order_id} not found for Table {table_id}")
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        log.error(f"Error updating order {order_id} for Table {table_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Updating order {order_id} for Table {table_id} ended")


@app.route('/table/<int:table_id>/order/<int:order_id>', methods=['DELETE'])
def delete_table_order(table_id, order_id):
    """
    Endpoint to delete a specific order for a specific table.
    Logs the action, checks if the table and order exist, and deletes the order.
    Handles exceptions and logs errors.
    """
    try:
        if table_id in TABLES and order_id in TABLES[table_id]["orders"]:
            log.info(f"Deleting order {order_id} for Table {table_id} started")
            del TABLES[table_id]["orders"][order_id]
            log.info(f"Order {order_id} deleted for Table {table_id} and remaining orders are"
                     f" {TABLES[table_id]['orders']}")
            return jsonify({"status": "Order deleted"})
        else:
            log.warning(f"Order {order_id} not found for Table {table_id}")
            return jsonify({"error": "Order not found"}), 404
    except Exception as e:
        log.error(f"Error deleting order {order_id} for Table {table_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Deleting order {order_id} for Table {table_id} ended")


@app.route('/table/<int:table_id>/billing', methods=['GET'])
def get_table_billing(table_id):
    """
    Endpoint to get the billing for a specific table.
    Logs the action, checks if the table exists, calculates the total bill, and returns it.
    Handles exceptions and logs errors.
    """
    try:
        if table_id in TABLES:
            log.info(f"Calculating billing for Table {table_id} started")
            total_bill = 0
            orders = TABLES[table_id]["orders"]
            for order_id, order in orders.items():
                for item in order["items"]:
                    category, item_name = item["category"], item["name"]
                    total_bill += MENU[category][item_name] * item["quantity"]
            log.info(f"Billing calculated for Table {table_id}: Total Bill = {total_bill}")
            return jsonify({"table_id": table_id, "total_bill": total_bill})
        else:
            log.warning(f"Table {table_id} not found")
            return jsonify({"error": "Table not found"}), 404
    except Exception as e:
        log.error(f"Error calculating billing for Table {table_id}: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        log.info(f"Calculating billing for Table {table_id} ended")


if __name__ == '__main__':
    app.run(debug=True)
