from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import os

# Users may be either a guest, employee, manager, or admin
# guest: can view inventory
# employee: can view inventory, edit items
# manager: can view inventory, edit items, add items, remove items, add employee users, remove employee users, edit users
# admin: can view inventory, edit items, add items, remove items and users, edit users, add managers, remove managers, edit managers
class UserManager:
    def __init__(self):
        self.users = []
        self.sessions = []
        self.next_id = 0
        
        self.filepath = "data/users.json"
        # if file doesn't path exist and create it if it doesn't
        if not os.path.exists(self.filepath):
            self.save_users()

        self.load_users()

    def load_users(self):
        with open(self.filepath, "r") as file:
            data = json.load(file)
            self.users = data.get("users", [])
            self.next_id = data.get("next_id", 0)

    def save_users(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        with open(self.filepath, "w") as file:
            json.dump({"users": self.users, "next_id": self.next_id}, file, indent=4)

    def add_user(self, data):
        # Check if required data was provided
        if not data:
            return {"error": "No data provided"}, 400
        
        if "username" not in data:
            return {"error": "Username is required"}, 400
        
        if "email" not in data:
            return {"error": "Email is required"}, 400
        
        if "password" not in data:
            return {"error": "Password is required"}, 400
        
        if "role" not in data:
            return {"error": "Role is required"}, 400
        
        # Check if email already exists
        new_email = data["email"]
        if any(user["email"] == new_email for user in self.users):
            return {"error": "Email already exists"}, 400

        # Check if role is valid
        valid_roles = ["guest", "employee", "manager", "admin"]
        if data["role"] not in valid_roles:
            return {"error": "Invalid role"}, 400

        user = {
            "id": self.next_id,
            "username": data["username"],
            "email": data["email"],
            "password": data["password"],
            "role": data["role"],
        }

        self.users.append(user)
        self.next_id += 1
        self.save_users()
    
        return {"message": "User added successfully", "user": user}, 201

    def delete_user(self, user_id):        
        target_user = None
        for user in self.users:
            if user["id"] == user_id:
                target_user = user
                break
                
        if target_user is None:
            return {"error": "User not found"}, 404   
                
        # Remove user
        self.users.remove(user)
        
        # Save Changes
        self.save_users()
        return {"message": f"User with ID {user_id} removed successfully"}, 200
            

    def edit_user(self, data):
        # Check if required data was provided
        if not data:
            return {"error": "No data provided"}, 400
        
        if "username" not in data:
            return {"error": "Username is required"}, 400
        
        if "email" not in data:
            return {"error": "Email is required"}, 400
        
        if "password" not in data:
            return {"error": "Password is required"}, 400
        
        if "role" not in data:
            return {"error": "Role is required"}, 400
        
        # Find user by ID
        target_user = None
        for user in self.users:
            if user["id"] == data["id"]:
                target_user = user
                break
                
        if target_user is None:
            return {"error": "User not found"}, 404
            
        # Update user data
        # Check if email was changed and if new email already exists
        new_email = data["email"]
        if user["email"] != new_email and any(user["email"] == new_email for user in self.users):
            return {"error": "Email already exists"}, 400

        user["username"] = data["username"]
        user["email"] = data["email"]
        user["role"] = data["role"]
        user["password"] = data["password"] 

        # Save Changes
        self.save_users()
        return {
            "message": f"User with ID {data['id']} updated successfully",
            "user": user,
        }, 200
        
    def login(self, username, password):
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                # Generate a simple session token (in production, use a secure method)
                session_token = f"{user['id']}-{username}"
                self.sessions.append({"token": session_token, "user_id": user["id"]})
                return {"token": session_token, "role": user["role"]}, 200
        return {"error": "Invalid credentials"}, 401

    def verify_session(self, token):
        for session in self.sessions:
            if session["token"] == token:
                for user in self.users:
                    if user["id"] == session["user_id"]:
                        return user["role"]
        return None


class InventoryManager:
    def __init__(self):

            
        self.inventory = []
        self.next_id = 0
        
        self.filepath = "data/inventory.json"
        if not os.path.exists(self.filepath):
            self.save_inventory()
            
        self.load_inventory()
        
    # load from json file
    def load_inventory(self):
        with open(self.filepath, "r") as file:
            data = json.load(file)
            self.inventory = data.get("inventory", [])
            self.next_id = data.get("next_id", 0)

    # Save inventory to json file
    def save_inventory(self):
        # Create file path if it doesn't exist
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        
        # Write to file
        with open(self.filepath, "w") as file:
            json.dump(
            {"inventory": self.inventory, "next_id": self.next_id}, file, indent=4
            )

    # add item
    def add_item(self, data):
        # Check if required data was provided
        if not data:
            return {"error": "No data provided"}, 400
        
        if "name" not in data:
            return {"error": "Product name is required"}, 400
        
        if "quantity" not in data:
            return {"error": "Quantity is required"}, 400
        
        if "price" not in data:
            return {"error": "Price is required"}, 400
        
        if "color" not in data:
            return {"error": "Color is required"}, 400

        # Create item to inventory
        item = {
            "id": self.next_id,
            "name": data["name"],
            "quantity": int(data["quantity"]),
            "price": float(data["price"]),
            "color": data["color"],
        }
        
        # Save item to inventory
        self.inventory.append(item)
        self.next_id += 1
        self.save_inventory()
        
        return {"message": "Item added successfully", "item": item}, 201

    def remove_item(self, item_id):
        target_item = None
        for item in self.inventory:
            if item["id"] == item_id:
                target_item = item
                break
                
        self.inventory.remove(item)
        self.save_inventory()  # save inventory to edit file
        return {"message": f"Item with ID {item_id} removed successfully"}, 200
        return {"error": "Item not found"}, 404

    def edit_item(self, data):
        if (
            "id" not in data
            or "quantity" not in data
            or "price" not in data
            or "color" not in data
        ):
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
                self.save_inventory()  # save inventory to remove from file
                return {
                    "message": f"Item with ID {item_id} updated successfully",
                    "item": item,
                }, 200
        return {"error": "Item not found"}, 404

    def get_inventory(self, amount, skip, filters):
        filtered_inventory = self.inventory.copy()
        # TODO: Apply filters
        paginated_inventory = filtered_inventory[skip : skip + amount]
        return paginated_inventory


# flask app class
class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        self.inventory_manager = InventoryManager()
        self.user_manager = UserManager()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def home():
            return render_template("inventory.html")

        @self.app.route("/login")
        def login():
            return render_template("login.html")

        @self.app.route("/users")
        def users():
            return render_template("users.html")

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

        @self.app.route("/api/login", methods=["POST"])
        def api_login():
            username = request.args.get("username")
            password = request.args.get("password")
            if not username or not password:
                return jsonify({"error": "Username and password required"}), 400

            response, status_code = self.user_manager.login(username, password)
            return jsonify(response), status_code

        @self.app.route("/api/users", methods=["GET"])
        def get_users():
            # Verify admin/manager authorization here
            return jsonify(self.user_manager.users)

        @self.app.route("/api/users/add", methods=["POST"])
        def add_user():
            # Verify admin/manager authorization here
            data = request.json
            response, status_code = self.user_manager.add_user(data)
            return jsonify(response), status_code

        @self.app.route("/api/users/remove", methods=["DELETE"])
        def remove_user():
            # Verify admin/manager authorization here
            data = request.json
            
            if "id" not in data:
                return jsonify({"error": "ID is required"}), 400
            
            response, status_code = self.user_manager.delete_user(data["id"])
            return jsonify(response), status_code

        @self.app.route("/api/users/edit", methods=["POST"])
        def edit_user():
            # Verify admin/manager authorization here
            data = request.json
            response, status_code = self.user_manager.edit_user(data)
            return jsonify(response), status_code

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.run()
