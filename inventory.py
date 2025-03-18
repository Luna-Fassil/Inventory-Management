# IMPORTS FOR FLASK
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os

class InventoryManager:
    def __init__(self):
        self.filepath = "inventory.json" #saves inventory to json file instead of locally
        self.inventory = []
        self.next_id = 0
        self.load_inventory()

    #load inventory function 
    def load_inventory(self):
        if os.path.exists(self.filepath):#if json file exists
            with open(self.filepath, "r") as file:
                #try to load json file first 
                try:
                    data = json.load(file)
                    self.inventory = data.get("inventory", [])
                    self.next_id = data.get("next_id", 0)
                except json.JSONDecodeError:
                    self.inventory = []
                    self.next_id = 0
        else:#create a new one 
            self.save_inventory()

    #save inventory to json file
    def save_inventory(self):
        with open(self.filepath, "w") as file:#write to file 
            json.dump({"inventory": self.inventory, "next_id": self.next_id}, file, indent=4)#tab between info 

    #add item 
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
        self.save_inventory()#save inventory to write to file
        return {"message": "Item added successfully", "item": item}, 201

    def remove_item(self, item_id):
        for item in self.inventory:
            if item["id"] == item_id:
                self.inventory.remove(item)
                self.save_inventory()#save inventory to edit file
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
                self.save_inventory()#save inventory to remove from file
                return {"message": f"Item with ID {item_id} updated successfully", "item": item}, 200
        return {"error": "Item not found"}, 404

    def get_inventory(self, amount, skip, filters):
        filtered_inventory = self.inventory.copy()
        # TODO: Apply filters
        paginated_inventory = filtered_inventory[skip : skip + amount]
        return paginated_inventory


#flask app class
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

        @self.app.route("/login")
        def login():
            return render_template("login.html")

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