from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import os
import random


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
        self.default_password = "password"

        self.filepath = "data/users.json"
        # if file doesn't path exist and create it if it doesn't
        if not os.path.exists(self.filepath):
            self.save_users()

        self.load_users()

        # Create default admin user if no users exist
        if len(self.users) == 0:
            print("Hello")
            for user in [
                {
                    "id": 0,
                    "username": "admin",
                    "email": "admin@email.com",
                    "password": "password",
                    "role": "admin",
                },
                {
                    "id": 1,
                    "username": "manager", 
                    "email": "manager@email.com",
                    "password": "password",
                    "role": "manager",
                },
                {
                    "id": 2,
                    "username": "employee",
                    "email": "employee@email.com", 
                    "password": "password",
                    "role": "employee",
                },
                {
                    "id": 3,
                    "username": "guest",
                    "email": "guest@email.com",
                    "password": "password",
                    "role": "guest",
                }
            ]:
                self.users.append(user)
            self.save_users()

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

        if len(self.users) <= 1:
            return {"error": "Cannot remove last user"}, 400

        # check that not deleting the last admin
        # Count number of admin users (excluding the one being deleted)
        admin_count = sum(1 for user in self.users if user["role"] == "admin")
        if admin_count <= 1 and target_user["role"] == "admin": 
            return {"error": "Cannot remove last admin user"}, 400

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

        if data["role"] != "admin" and all(
            user["role"] == "admin" for user in self.users
        ):
            return {"error": "Cannot remove last admin user"}, 400

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
        if user["email"] != new_email and any(
            user["email"] == new_email for user in self.users
        ):
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
        found_user = None
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                found_user = user

        # Generate a simple session token (in production, use a secure method)
        if found_user is not None:
            session_token = f"{found_user['id']}{username}{random.randint(0, 9999)}"
            self.sessions.append({"token": session_token, "user_id": found_user["id"]})
            return {"token": session_token, "role": found_user["role"]}, 200

        return {"error": "Invalid credentials"}, 401

    def verify_session(self, token):
        print(self.sessions)
        for session in self.sessions:
            if session["token"] == token:
                print(session)
                for user in self.users:
                    print(user)
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

        if "token" not in data:
            return {"error": "Token is required"}, 400

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

    def get_inventory(self, data):
        if not data:
            data = {}

        if "skip" in data:
            skip = int(data["skip"])
        else:
            skip = 0

        if "amount" in data:
            amount = int(data["amount"])
        else:
            amount = 100

        if "sort" in data:
            sort = data["sort"]
        else:
            sort = "id"

        if "filters" in data:
            pass
            # TODO: Apply filters

        filtered_inventory = self.inventory.copy()
        paginated_inventory = filtered_inventory[skip : skip + amount]
        return paginated_inventory, 200


# flask app class
class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        self.inventory_manager = InventoryManager()
        self.user_manager = UserManager()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/inventory")
        def home():
            return render_template("inventory.html")

        @self.app.route("/")
        def login():
            return render_template("login.html")

        @self.app.route("/users")
        def users():
            return render_template("users.html")

        @self.app.route("/inventory", methods=["POST"])
        def get_inventory():
            data = request.json

            response, status_code = self.inventory_manager.get_inventory(data)
            return jsonify(response), status_code

        @self.app.route("/add", methods=["POST"])
        def add_item():
            data = request.json

            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400

            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401

            response, status_code = self.inventory_manager.add_item(data)
            return jsonify(response), status_code

        @self.app.route("/remove", methods=["DELETE"])
        def remove_item():
            data = request.json
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400

            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401

            response, status_code = self.inventory_manager.remove_item(data["id"])
            return jsonify(response), status_code

        @self.app.route("/edit", methods=["POST"])
        def edit_item():
            data = request.json

            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400

            if not authorization(data["token"], ["employee", "admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401

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
            return jsonify(self.user_manager.users)

        @self.app.route("/api/users/add", methods=["POST"])
        def add_user():
            data = request.json
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401

            response, status_code = self.user_manager.add_user(data)
            return jsonify(response), status_code

        @self.app.route("/api/users/remove", methods=["DELETE"])
        def remove_user():
            data = request.json
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401

            response, status_code = self.user_manager.delete_user(data["id"])
            return jsonify(response), status_code

        @self.app.route("/api/users/edit", methods=["POST"])
        def edit_user():
            data = request.json
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            response, status_code = self.user_manager.edit_user(data)
            return jsonify(response), status_code

        def authorization(token, roles):
            user_role = self.user_manager.verify_session(token)
            print(user_role)
            if user_role not in roles:
                return False

            return True

    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.run()
