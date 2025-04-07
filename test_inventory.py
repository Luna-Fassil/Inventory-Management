import unittest
from inventory import InventoryManager

class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        """Set up a fresh instance of InventoryManager for each test."""
        self.inventory_manager = InventoryManager()
        self.inventory_manager.inventory = []
        self.inventory_manager.next_id = 0

    def test_add_item(self):
        # Test adding a valid item
        data = {
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        }
        response, status_code = self.inventory_manager.add_item(data)
        self.assertEqual(status_code, 201)
        self.assertEqual(response["message"], "Item added successfully")
        self.assertEqual(len(self.inventory_manager.inventory), 1)

        # Test adding an item with missing fields
        invalid_data = {"name": "Shirt", "quantity": 10}
        response, status_code = self.inventory_manager.add_item(invalid_data)
        self.assertEqual(status_code, 400)
        self.assertIn("is required", response["error"])

    def test_remove_item(self):
        # Add an item to the inventory
        data = {
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        }
        self.inventory_manager.add_item(data)

        # Test removing an existing item
        response, status_code = self.inventory_manager.remove_item(0)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "Item with ID 0 removed successfully")
        self.assertEqual(len(self.inventory_manager.inventory), 0)

        # Test removing a non-existent item
        response, status_code = self.inventory_manager.remove_item(99)
        self.assertEqual(status_code, 404)
        self.assertEqual(response["error"], "Item not found")

    def test_edit_item(self):
        # Add an item to the inventory
        data = {
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        }
        self.inventory_manager.add_item(data)

        # Test editing an existing item
        updated_data = {
            "id": 0,
            "name": "Pant",
            "quantity": 1,
            "price": 20,
            "color": "blue",
            "brand": "adidas",
            "season": "spring"
        }
        response, status_code = self.inventory_manager.edit_item(updated_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "Item with ID 0 updated successfully")
        self.assertEqual(self.inventory_manager.inventory[0]["name"], "Pant")
        self.assertEqual(self.inventory_manager.inventory[0]["quantity"], 1)

        # Test editing a non-existent item
        invalid_data = {
            "id": 99,
            "name": "Socks",
            "quantity": 5,
            "price": 2,
            "color": "yellow",
            "brand": "shein",
            "season": "summer"
        }
        response, status_code = self.inventory_manager.edit_item(invalid_data)
        self.assertEqual(status_code, 404)
        self.assertEqual(response["error"], "Item not found")

    def test_get_inventory(self):
        # Add some items to the inventory
        self.inventory_manager.add_item({
            "name": "Shirt",
            "quantity": 10,
            "price": 20,
            "color": "red",
            "brand": "nike",
            "season": "fall"
        })
        self.inventory_manager.add_item({
            "name": "Socks",
            "quantity": 5,
            "price": 2,
            "color": "yellow",
            "brand": "adidas",
            "season": "summer"
        })

        # Test getting the full inventory
        inventory = self.inventory_manager.get_inventory(amount=10, skip=0, filters={})
        self.assertEqual(len(inventory), 2)

        # Test pagination
        inventory = self.inventory_manager.get_inventory(amount=1, skip=0, filters={})
        self.assertEqual(len(inventory), 1)
        self.assertEqual(inventory[0]["name"], "Shirt")

if __name__ == "__main__":
    unittest.main()
