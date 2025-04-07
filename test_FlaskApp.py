import unittest
from flask import json
from inventory import FlaskApp

class TestFlaskApp(unittest.TestCase):
   def setUp(self):
    # create flask test client before each test
    self.flask_app = FlaskApp()
    self.app = self.flask_app.app.test_client()

    # login and store token
    login_response = self.app.post("/api/login?username=admin&password=password")
    self.token = json.loads(login_response.data)["token"]

    # clear the inventory before each test
    with open("inventory.json", "w") as f:
        f.write("[]")

    def test_home_route(self):
        # basic check if home route works
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_item_route(self):
        # try adding a valid item
        data = {
            "token": self.token,
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        }
        response = self.app.post("/api/inventory/add", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["message"], "Item added successfully")

        # try adding an invalid item with missing fields
        invalid_data = {
            "token": self.token,
            "name": "Shirt",
            "quantity": 10
        }
        response = self.app.post("/api/inventory/add", json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("is required", json.loads(response.data)["error"])

    def test_remove_item_route(self):
        # first, add an item to test removal
        data = {
            "token": self.token,
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        }
        add_response = self.app.post("/api/inventory/add", json=data)
        item_id = json.loads(add_response.data)["item"]["id"]

        # remove the existing item (id 0, since it's the first one added)
        response = self.app.delete("/api/inventory/remove", json={"token": self.token, "id": item_id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["message"], f"Item with ID {item_id} removed successfully")

        # try removing an item that doesn't exist
        response = self.app.delete("/api/inventory/remove", json={"token": self.token, "id": 99})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["error"], "Item not found")

    def test_edit_item_route(self):
        # add an item first to test editing
        data = {
            "token": self.token,
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        }
        add_response = self.app.post("/api/inventory/add", json=data)
        item_id = json.loads(add_response.data)["item"]["id"]

        # edit the item using its id
        updated_data = {
            "token": self.token,
            "id": item_id,
            "name": "Pant",
            "quantity": 1,
            "price": 20,
            "color": "blue",
            "brand": "adidas",
            "season": "spring"
        }
        response = self.app.post("/api/inventory/edit", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["message"], f"Item with ID {item_id} updated successfully")

        # try editing a non-existent item
        invalid_data = {
            "token": self.token,
            "id": 99,
            "name": "Socks",
            "quantity": 5,
            "price": 2,
            "color": "yellow",
            "brand": "shein",
            "season": "summer"
        }
        response = self.app.post("/api/inventory/edit", json=invalid_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["error"], "Item not found")

    def test_get_inventory_route(self):
        # add two items to test inventory retrieval
        self.app.post("/api/inventory/add", json={
            "token": self.token,
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        })
        self.app.post("/api/inventory/add", json={
            "token": self.token,
            "name": "Socks",
            "quantity": 5,
            "price": 2,
            "color": "yellow",
            "brand": "adidas",
            "season": "summer"
        })

        # get the full inventory list
        response = self.app.post("/api/inventory", json={"token": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 2)

        # test pagination using query params (?amount=1&skip=0)
        response = self.app.post("/api/inventory", json={"token": self.token, "amount": 1, "skip": 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1)
        self.assertEqual(json.loads(response.data)[0]["name"], "Shirt")

if __name__ == "__main__":
    unittest.main()
