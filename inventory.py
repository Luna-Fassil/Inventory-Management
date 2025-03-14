# Backend code -> add Iteration 1 Functions here

# IMPORTS FOR FLASK
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # allow frontend JavaScript to make API requests

# temp in memory storage for inventory
inventory = []
next_id = 0


@app.route("/")
def home():
    return render_template("inventory.html")  # flask will use HTML File

@app.route("/login")
def login():
    return render_template("login.html")  # flask will use HTML File


@app.route("/inventory", methods=["GET"])
def get_inventory():
    amount = request.args.get("amount", default=100, type=int)
    skip = request.args.get("skip", default=0, type=int)
    filters = request.args.get("filters", "{}")
    filters = json.loads(filters)

    # TODO filter inventory for on existing filters
    print(filters)
    filtered_inventory = inventory.copy()

    # Apply pagination
    paginated_inventory = filtered_inventory[skip : skip + amount]
    return jsonify(paginated_inventory)

# old filter code for refrence
# async function fetchResults(skip, amount, filters) {
#   let results = inventory.slice();

#   if (filters.search) {
#     results = results.filter(
#       (item) => item.name.includes(filters.search) || item.id == filters.search
#     );
#   }

#   if (filters.maxPrice) {
#     results = results.filter((item) => item.price < filters.maxPrice);
#   }

#   if (filters.minPrice) {
#     results = results.filter((item) => item.price > filters.minPrice);
#   }

#   if (filters.maxQuantity) {
#     results = results.filter((item) => item.quantity < filters.maxQuantity);
#   }

#   if (filters.minQuantity) {
#     results = results.filter((item) => item.quantity > filters.minQuantity);
#   }

#   if (filters.color) {
#     results = results.filter((item) => item.color == filters.color);
#   }

#   return results.slice(skip, amount);
# }


# TODO: SAVE INVENTORY TO A FILE SO THAT IT DOESnT GO AWAY WHEN REFRESHED
@app.route("/add", methods=["POST"])
def add_item():
    global next_id

    data = request.json

    # make sure all fields filled out or error
    if not data or not all(k in data for k in ("name", "quantity", "price", "color")):
        return jsonify({"error": "Missing required fields"}), 400

    # saved data of item assigns id, name, quantity, price and colour which are stated requirement
    item = {
        "id": next_id,
        "name": data["name"],
        "quantity": int(data["quantity"]),
        "price": float(data["price"]),
        "color": data["color"],
    }
    inventory.append(item)  # add item to inventory
    next_id += 1  # go to next id so no items have same one

    return jsonify(
        {"message": "Item added successfully", "item": item}
    ), 201  # alert item added


# route to handle removing an item from the inventory
@app.route("/remove", methods=["DELETE"])
def remove_item():
    data = request.json
    if "id" not in data:
        return jsonify(
            {"error": "ID is required"}
        ), 400  # return error if ID is missing

    item_id = data["id"]

    # find item in inventory through iteration
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)  # remove the item from the inventory
            return jsonify(
                {"message": f"Item with ID {item_id} removed successfully"}
            ), 200
    # return an error if no matching item was found
    return jsonify({"error": "Item not found"}), 404


@app.route("/edit", methods=["POST"])
def edit_item():
    data = request.json
    print("Received Data:", data)  # Debugging: Log the received data

    if (
        "id" not in data
        or "quantity" not in data
        or "price" not in data
        or "color" not in data
    ):
        return jsonify(
            {"error": "ID, quantity, price, and color are required"}
        ), 400  # return error if any field is missing

    item_id = data["id"]
    new_name = data["name"]
    new_quantity = int(data["quantity"])
    new_price = float(data["price"])
    new_color = data["color"]

    # find item in inventory
    for item in inventory:
        if item["id"] == item_id:
            print("Found Item:", item)  # Debugging: Log the item before updating
            item["name"] = new_name
            item["quantity"] = new_quantity  # update the quantity of the item
            item["price"] = new_price  # update the price of the item
            item["color"] = new_color  # update the color of the item
            print("Updated Item:", item)  # Debugging: Log the item after updating
            return jsonify(
                {
                    "message": f"Item with ID {item_id} updated successfully",
                    "item": item,
                }
            ), 200

    # return an error if no matching item was found
    return jsonify({"error": "Item not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
