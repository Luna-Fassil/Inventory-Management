import unittest
from flask import json
from inventory import FlaskApp

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        # create flask test client before each test
        self.flask_app = FlaskApp()
        self.app = self.flask_app.app.test_client()

    def test_home_route(self):
        # basic check if home route works
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_add_item_route(self):
        # try adding a valid item
        data = {"name": "Shirt", "quantity": 10, "price": 20, "color": "red"}
        response = self.app.post("/add", json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)["message"], "Item added successfully")

        # try adding an invalid item with missing fields
        invalid_data = {"name": "Shirt", "quantity": 10}
        response = self.app.post("/add", json=invalid_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data)["error"], "Missing required fields")

    def test_remove_item_route(self):
        # first, add an item to test removal
        data = {"name": "Shirt", "quantity": 10, "price": 20, "color": "red"}
        self.app.post("/add", json=data)

        # remove the existing item (id 0, since it's the first one added)
        response = self.app.delete("/remove", json={"id": 0})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["message"], "Item with ID 0 removed successfully")

        # try removing an item that doesn't exist
        response = self.app.delete("/remove", json={"id": 99})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["error"], "Item not found")

    def test_edit_item_route(self):
        # add an item first to test editing
        data = {"name": "Shirt", "quantity": 10, "price": 20, "color": "red"}
        self.app.post("/add", json=data)

        # edit the item using its id
        updated_data = {"id": 0, "name": "Pant", "quantity": 1, "price": 20, "color": "blue"}
        response = self.app.post("/edit", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)["message"], "Item with ID 0 updated successfully")

        # try editing a non-existent item
        invalid_data = {"id": 99, "name": "Socks", "quantity": 5, "price": 2, "color": "yellow"}
        response = self.app.post("/edit", json=invalid_data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data)["error"], "Item not found")

    def test_get_inventory_route(self):
        # add two items to test inventory retrieval
        self.app.post("/add", json={"name": "Shirt", "quantity": 10, "price": 20, "color": "red"})
        self.app.post("/add", json={"name": "Socks", "quantity": 5, "price": 2, "color": "yellow"})

        # get the full inventory list
        response = self.app.get("/inventory")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 2)

        # test pagination using query params (?amount=1&skip=0)
        response = self.app.get("/inventory?amount=1&skip=0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.data)), 1)
        self.assertEqual(json.loads(response.data)[0]["name"], "Shirt")

if __name__ == "__main__":
    unittest.main()
