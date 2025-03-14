import unittest
from flask import json
from inventory import FlaskApp

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client."""
        self.flask_app = FlaskApp()
        self.app = self.flask_app.app.test_client()

    def test_home_route(self):
        # Test the home route
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_item_route(self):
        # Test adding an item via the /add route
        data = {"name": "Apple", "quantity": 10, "price": 1.99, "color": "red"}
        response = self.app.post("/add", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["message"], "Item added successfully")

        # Test adding an item with missing fields
        invalid_data = {"name": "Banana", "quantity": 5}
        response = self.app.post("/add", json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)["error"], "Missing required fields")

    def test_remove_item_route(self):
        # Add an item to the inventory
        data = {"name": "Apple", "quantity": 10, "price": 1.99, "color": "red"}
        self.app.post("/add", json=data)

        # Test removing an existing item
        response = self.app.delete("/remove", json={"id": 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["message"], "Item with ID 0 removed successfully")

        # Test removing a non-existent item
        response = self.app.delete("/remove", json={"id": 99})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["error"], "Item not found")

    def test_edit_item_route(self):
        # Add an item to the inventory
        data = {"name": "Apple", "quantity": 10, "price": 1.99, "color": "red"}
        self.app.post("/add", json=data)

        # Test editing an existing item
        updated_data = {"id": 0, "name": "Green Apple", "quantity": 15, "price": 2.99, "color": "green"}
        response = self.app.post("/edit", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["message"], "Item with ID 0 updated successfully")

        # Test editing a non-existent item
        invalid_data = {"id": 99, "name": "Banana", "quantity": 5, "price": 0.99, "color": "yellow"}
        response = self.app.post("/edit", json=invalid_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["error"], "Item not found")

    def test_get_inventory_route(self):
        # Add some items to the inventory
        self.app.post("/add", json={"name": "Apple", "quantity": 10, "price": 1.99, "color": "red"})
        self.app.post("/add", json={"name": "Banana", "quantity": 5, "price": 0.99, "color": "yellow"})

        # Test getting the full inventory
        response = self.app.get("/inventory")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 2)

        # Test pagination
        response = self.app.get("/inventory?amount=1&skip=0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1)

if __name__ == "__main__":
    unittest.main()