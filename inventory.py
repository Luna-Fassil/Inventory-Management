# IMPORTS FOR FLASK
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

class InventoryManager:
    def __init__(self):
        self.inventory = []
        self.next_id = 0

    def add_item(self, data):
        if not data or not all(k in data for k in ("name", "quantity", "price", "color")):
            return {"error": "Missing required fields"}, 400

        item = {
            "id": self.next_id,
            "name": data["name"],
            "quantity": int(data["quantity"]),
            "price": float(data["price"]),
            "color": data["color"],
        }
        self.inventory.append(item)
        self.next_id += 1
        return {"message": "Item added successfully", "item": item}, 201

    def remove_item(self, item_id):
        for item in self.inventory:
            if item["id"] == item_id:
                self.inventory.remove(item)
                return {"message": f"Item with ID {item_id} removed successfully"}, 200
        return {"error": "Item not found"}, 404

    def edit_item(self, data):
        if "id" not in data or "quantity" not in data or "price" not in data or "color" not in data:
            return {"error": "ID, quantity, price, and color are required"}, 400

        item_id = data["id"]
        new_name = data["name"]
        new_quantity = int(data["quantity"])
        new_price = float(data["price"])
        new_color = data["color"]

        for item in self.inventory:
            if item["id"] == item_id:
                item["name"] = new_name
                item["quantity"] = new_quantity
                item["price"] = new_price
                item["color"] = new_color
                return {"message": f"Item with ID {item_id} updated successfully", "item": item}, 200
        return {"error": "Item not found"}, 404

    def get_inventory(self, amount, skip, filters):
        filtered_inventory = self.inventory.copy()
        # TODO: Apply filters
        paginated_inventory = filtered_inventory[skip : skip + amount]
        return paginated_inventory

class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)
        self.inventory_manager = InventoryManager()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def home():
            return render_template("inventory.html")

        @self.app.route("/inventory", methods=["GET"])
        def get_inventory():
            amount = request.args.get("amount", default=100, type=int)
            skip = request.args.get("skip", default=0, type=int)
            filters = request.args.get("filters", "{}")
            filters = json.loads(filters)
            inventory = self.inventory_manager.get_inventory(amount, skip, filters)
            return jsonify(inventory)

        @self.app.route("/add", methods=["POST"])
        def add_item():
            data = request.json
            response, status_code = self.inventory_manager.add_item(data)
            return jsonify(response), status_code

        @self.app.route("/remove", methods=["DELETE"])
        def remove_item():
            data = request.json
            if "id" not in data:
                return jsonify({"error": "ID is required"}), 400
            response, status_code = self.inventory_manager.remove_item(data["id"])
            return jsonify(response), status_code

        @self.app.route("/edit", methods=["POST"])
        def edit_item():
            data = request.json
            response, status_code = self.inventory_manager.edit_item(data)
            return jsonify(response), status_code

    def run(self):
        self.app.run(debug=True)

if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.run()