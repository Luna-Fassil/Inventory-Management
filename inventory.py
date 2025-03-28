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
        self.next_id = 0
        self.default_users = [
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
            },
        ]

        self.storage_path = "data/users.json"
        if not os.path.exists(self.storage_path):
            self.save_users()
            
        self.sessions = []
        self.load_users()
        
        # Create default users if no users exist
        if len(self.users) == 0:
            self.users = self.default_users
            self.next_id = len(self.users)
            self.save_users()

    def load_users(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        with open(self.storage_path, "r") as file:
            data = json.load(file)
            self.users = data.get("users", [])
            self.next_id = data.get("next_id", 0)

    def save_users(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        with open(self.storage_path, "w") as file:
            json.dump({"users": self.users, "next_id": self.next_id}, file, indent=4)

    def add_user(self, data):
        # Check if required data was provided
        if not data:
            return {"error": "No data provided"}, 400

        required_fields = ["username", "email", "password", "role"]
        for field in required_fields:
            if field not in data:
                return {"error": f"{field.title()} is required"}, 400

        # Check if email already exists
        new_email = data["email"]
        if any(user["email"] == new_email for user in self.users):
            return {"error": "Email already exists"}, 400

        # Check if role is valid
        valid_roles = ["guest", "employee", "manager", "admin"]
        if data["role"] not in valid_roles:
            return {"error": "Invalid role"}, 400

        # Add new user
        user = {
            "id": self.next_id,
            "username": data["username"],
            "email": data["email"],
            "password": data["password"],
            "role": data["role"],
        }
        self.users.append(user)
        self.save_users()
        self.next_id += 1
        
        # return the newly created user
        return {"message": "User added successfully", "user": user}, 201

    def delete_user(self, user_id):
        # Search for specified user
        target_user = None
        for user in self.users:
            if user["id"] == user_id:
                target_user = user
                break

        if target_user is None:
            return {"error": "User not found"}, 404

        # Ensure there is always one admin
        admin_count = sum(1 for user in self.users if user["role"] == "admin")
        if admin_count <= 1 and target_user["role"] == "admin":
            return {"error": "Cannot remove last admin user"}, 400

        # Remove user
        self.users.remove(user)
        self.save_users()

        return {"message": f"User with ID {user_id} removed successfully"}, 200

    def edit_user(self, data):
        # Check if required data was provided
        if not data:
            return {"error": "No data provided"}, 400

        required_fields = ["username", "email", "password", "role"]
        for field in required_fields:
            if field not in data:
                return {"error": f"{field.title()} is required"}, 400

        # Find user by ID
        target_user = None
        for user in self.users:
            if user["id"] == data["id"]:
                target_user = user
                break

        if target_user is None:
            return {"error": "User not found"}, 404

        # Ensure you don't edit the last admin
        admin_count = sum(1 for user in self.users if user["role"] == "admin")
        if (                                # if
            target_user["role"] == "admin"  # editing an admin
            and data["role"] != "admin"     # to not an admin
            and admin_count <= 1            # and they are the last admin
        ):                                  # error
            return {"error": "Cannot remove last admin user"}, 400

        # Ensure new email doesn't already exists
        new_email = data["email"]
        if user["email"] != new_email and any(
            user["email"] == new_email for user in self.users
        ):
            return {"error": "Email already exists"}, 400

        # Update user data
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
        # Search for user matchin credentials
        found_user = None
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                found_user = user
        if found_user is None:
            return {"error": "Invalid credentials"}, 401
            
        # generate a session for the user
        session_token = f"{user['id']}-{random.randint(0, 99999)}-{random.randint(0, 99999)}-{random.randint(0, 99999)}"
        self.sessions.append({"token": session_token, "user_id": found_user["id"]})
        return {"token": session_token, "role": found_user["role"]}, 200
        
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

        self.storage_path = "data/inventory.json"
        if not os.path.exists(self.storage_path):
            self.save_inventory()

        self.load_inventory()

    # load from json file
    def load_inventory(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        with open(self.storage_path, "r") as file:
            data = json.load(file)
            self.inventory = data.get("inventory", [])
            self.next_id = data.get("next_id", 0)

    # Save inventory to json file
    def save_inventory(self):
        # Create file path if it doesn't exist
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

        # Write to file
        with open(self.storage_path, "w") as file:
            json.dump(
                {"inventory": self.inventory, "next_id": self.next_id}, file, indent=4
            )

    # add item
    def add_item(self, data):
        # Check if required data was provided
        if not data:
            return {"error": "No data provided"}, 400

        required_fields = ["name", "quantity", "price", "color", "brand", "season"]
        for field in required_fields:
            if field not in data:
                return {"error": f"{field.capitalize()} is required"}, 400

        # Create item to inventory
        item = {
            "id": self.next_id,
            "name": data["name"],
            "quantity": int(data["quantity"]),
            "price": float(data["price"]),
            "color": data["color"],
            "brand": data["brand"],
            "season": data["season"],
        }

        # Save item to inventory
        self.inventory.append(item)
        self.next_id += 1
        self.save_inventory()

        return {"message": "Item added successfully", "item": item}, 201

    def remove_item(self, item_id):
        # Find Specified Item
        target_item = None
        for item in self.inventory:
            if item["id"] == item_id:
                target_item = item
                break
        if target_item == None:
            return {"error": "Item not found"}, 404

        # Remove the item
        self.inventory.remove(item)
        self.save_inventory()
        
        return {"message": f"Item with ID {item_id} removed successfully"}, 200

    def edit_item(self, data):
        # Check if required data was provided
        if not data:
            return {"error": "No data provided"}, 400

        required_fields = ["id", "name", "quantity", "price", "color", "brand", "season"]
        for field in required_fields:
            if field not in data:
                return {"error": f"{field.capitalize()} is required"}, 400

        # Find item targeted by edits
        target_item = None
        for item in self.inventory:
            if item["id"] == data["id"]:
                target_item = item
        
        if target_item == None:
            return {"error": "Item not found"}, 404
                
        # Edit Item
        target_item["name"] = data["name"]
        target_item["quantity"] = int(data["quantity"])
        target_item["price"] = float(data["price"])
        target_item["color"] = data["color"]
        target_item["brand"] = data["brand"]
        target_item["season"] = data["season"]
        self.save_inventory()
        
        return {
            "message": f"Item with ID {data['id']} updated successfully",
            "item": item,
        }, 200

    def get_inventory(self, amount, skip, sort, filters):
        filtered_inventory = self.inventory.copy()

        # search filter
        if "search" in filters and filters["search"]:
            filtered_inventory = self.search_item(filters["search"])

        # TODO: Apply filters
        
        paginated_inventory = filtered_inventory[skip : skip + amount]
        return paginated_inventory

    # COMMENT OUT TO FAIL TDD TEST
    # search inventory by name (case-insensitive, allows partial match)
    def search_item(self, query):
        # search by name (partial, case-insensitive) or ID (exact match)
        query = query.strip().lower()
        # hold results in array
        results = []
        for item in self.inventory:
            # match by ID if query is a digit
            if query.isdigit() and int(query) == item["id"]:
                results.append(item)
                continue
            # match by partial name
            if query in item["name"].lower():
                results.append(item)
        return results


# flask app class
class FlaskApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

        self.inventory_manager = InventoryManager()
        self.user_manager = UserManager()
        self.setup_routes()

    def setup_routes(self):
        #########
        # Pages #
        #########
        @self.app.route("/")
        def login():
            return render_template("login.html")

        @self.app.route("/inventory")
        def inventory():
            return render_template("inventory.html")

        @self.app.route("/users")
        def users():            
            return render_template("users.html")
        
        @self.app.route("/settings")
        def settings():            
            return render_template("settings.html")

        #################
        # Inventory API #
        #################
        @self.app.route("/api/inventory", methods=["GET", "POST"])
        def get_inventory():
            data = request.json
            
            # Validate user
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400
            
            if not authorization(data["token"], ["guest","employee","admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            
            amount = data.get("amount", 100)
            skip = data.get("skip", 0)
            sort = data.get("sort", "id")
            filters = data.get("filters", {})
            
            # Handle response
            inventory = self.inventory_manager.get_inventory(amount, skip, sort, filters)
            return jsonify(inventory)

        @self.app.route("/api/inventory/add", methods=["POST"])
        def add_item():
            data = request.json
            
            # Validate user
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400
            
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            
            # Handle response
            response, status_code = self.inventory_manager.add_item(data)
            return jsonify(response), status_code

        @self.app.route("/api/inventory/remove", methods=["DELETE"])
        def remove_item():
            data = request.json
            
            # Validate User
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400

            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            
            # Handle response
            response, status_code = self.inventory_manager.remove_item(data["id"])
            return jsonify(response), status_code

        @self.app.route("/api/inventory/edit", methods=["POST"])
        def edit_item():
            data = request.json
            
            # Validate User
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400

            if not authorization(data["token"], ["employee", "admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            
            # Handle response
            response, status_code = self.inventory_manager.edit_item(data)
            return jsonify(response), status_code


        #############
        # Users API #
        #############
        @self.app.route("/api/login", methods=["POST"])
        def api_login():
            username = request.args.get("username")
            password = request.args.get("password")
            
            if not username or not password:
                return jsonify({"error": "Username and password required"}), 400

            # Handel Response
            response, status_code = self.user_manager.login(username, password)
            return jsonify(response), status_code

        @self.app.route("/api/users", methods=["POST"])
        def get_users():
            data = request.json
            
            # Validate user
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400
            
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            
            # Handle response
            return jsonify(self.user_manager.users)

        @self.app.route("/api/users/add", methods=["POST"])
        def add_user():
            data = request.json
            
            # Validate user
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400
            
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            
            # Handle response
            response, status_code = self.user_manager.add_user(data)
            return jsonify(response), status_code

        @self.app.route("/api/users/remove", methods=["DELETE"])
        def remove_user():
            data = request.json
            
            # Validate User
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400
            
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401

            # Handle response
            response, status_code = self.user_manager.delete_user(data["id"])
            return jsonify(response), status_code

        @self.app.route("/api/users/edit", methods=["POST"])
        def edit_user():
            data = request.json
            
            # Validate User
            if "token" not in data:
                return jsonify({"error": "Token is required"}), 400
            
            if not authorization(data["token"], ["admin", "manager"]):
                return jsonify({"error": "Unauthorized"}), 401
            
            # Handle response
            response, status_code = self.user_manager.edit_user(data)
            return jsonify(response), status_code

        def authorization(token, roles):
            user_role = self.user_manager.verify_session(token)
            if user_role not in roles:
                return False
            return True
        
    def run(self):
        self.app.run(debug=True)


if __name__ == "__main__":
    flask_app = FlaskApp()
    flask_app.run()
