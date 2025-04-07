import unittest
from inventory import InventoryManager  # import inventory manager class

class TestInventorySearch(unittest.TestCase):
    def setUp(self):
        # initialize inventory with sample items
        self.manager = InventoryManager()
        self.manager.inventory = [
            {"id": 1, "name": "Skirt", "quantity": 10, "price": 999, "color": "blue", "brand": "nike", "season": "winter"},
            {"id": 2, "name": "Sweater", "quantity": 50, "price": 19, "color": "red", "brand": "adidas", "season": "spring"},
        ]

    def test_search_existing_item(self):
        # search by full name
        result = self.manager.search_item("Skirt")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Skirt")

    def test_search_partial_name(self):
        # search by partial name
        result = self.manager.search_item("Swea")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Sweater")

    def test_search_case_insensitive(self):
        # search should work with different cases
        result = self.manager.search_item("skirt")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "Skirt")

    def test_search_non_existent_item(self):
        # search for item that doesn't exist
        result = self.manager.search_item("Dog")
        self.assertEqual(len(result), 0)

    def test_search_by_id(self):
        # search using id as a string
        result = self.manager.search_item("1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    def test_search_blank_string(self):
        # search with empty string should return all items
        result = self.manager.search_item("")
        self.assertEqual(len(result), 2)

if __name__ == "__main__":
    unittest.main()

