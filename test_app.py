import unittest
import json
from inventory import app, inventory, next_id  # Import the Flask app and inventory list

class InventoryTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test client before each test."""
        self.app = app.test_client()
        self.app.testing = True

        # Clear the inventory and reset next_id before each test
        global inventory, next_id
        inventory.clear()
        next_id = 0

    def test_home(self):
        """Test the home page loads correctly."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_get_inventory_empty(self):
        """Test retrieving inventory when it's empty."""
        response = self.app.get("/inventory")
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    def test_add_item(self):
        """Test adding an item to inventory."""
        item_data = {
            "name": "Shirt",
            "quantity": 5,
            "price": 5,
            "color": "Red",
        }
        response = self.app.post("/add", data=json.dumps(item_data), content_type="application/json")
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertIn("message", data)
        self.assertEqual(data["item"]["name"], "Shirt")
        self.assertEqual(data["item"]["quantity"], 5)
        self.assertEqual(data["item"]["price"], 5)
        self.assertEqual(data["item"]["color"], "Red")


    def test_remove_item(self):
        """Test removing an item from inventory."""
        self.test_add_item()  # Add an item first
        response = self.app.delete("/remove", data=json.dumps({"id": 0}), content_type="application/json")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn("message", data)
        
    def test_edit_item(self):
        """Test editing an existing item in the inventory."""
        self.test_add_item()  # Add an item first
        updated_data = {
            "id": 0,
            "name": "Pant",
            "quantity": 10,
            "price": 10,
            "color": "Blue",
        }
        response = self.app.post("/edit", data=json.dumps(updated_data), content_type="application/json")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["item"]["name"], "Pant")
        self.assertEqual(data["item"]["quantity"], 10)
        self.assertEqual(data["item"]["price"], 10)
        self.assertEqual(data["item"]["color"], "Blue")

    def test_edit_item_not_found(self):
        """Test editing a non-existent item."""
        updated_data = {
            "id": 999,
            "name": "Pant",
            "quantity": 2,
            "price": 10,
            "color": "Black",
        }
        response = self.app.post("/edit", data=json.dumps(updated_data), content_type="application/json")
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertIn("error", data)

    

if __name__ == "__main__":
    unittest.main()
