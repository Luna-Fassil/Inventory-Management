import unittest
from inventory import UserManager

class TestUserManager(unittest.TestCase):
    def setUp(self):
        """Set up a fresh instance of UserManager for each test."""
        self.user_manager = UserManager()
        self.user_manager.users = []
        self.user_manager.next_id = 0

    def test_add_user(self):
        # Test adding a valid user
        data = {"username": "test_user", "password": "password123", "role": "employee", "email": "test@example.com"}
        response, status_code = self.user_manager.add_user(data)
        self.assertEqual(status_code, 201)
        self.assertEqual(response["message"], "User added successfully")
        self.assertEqual(len(self.user_manager.users), 1)

        # Test adding a user with missing fields
        invalid_data = {"username": "test_user2"}
        response, status_code = self.user_manager.add_user(invalid_data)
        self.assertEqual(status_code, 400)
        self.assertIn("is required", response["error"])

    def test_delete_user(self):
        # Add a user first
        data = {"username": "test_user", "password": "password123", "role": "employee", "email": "test@example.com"}
        self.user_manager.add_user(data)

        # Test deleting an existing user
        response, status_code = self.user_manager.delete_user(0)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "User with ID 0 removed successfully")
        self.assertEqual(len(self.user_manager.users), 0)

        # Test deleting a non-existent user
        response, status_code = self.user_manager.delete_user(99)
        self.assertEqual(status_code, 404)
        self.assertEqual(response["error"], "User not found")

    def test_edit_user(self):
        # Add a user first
        data = {"username": "test_user", "password": "password123", "role": "employee", "email": "test@example.com"}
        self.user_manager.add_user(data)

        # Test editing an existing user
        updated_data = {
            "id": 0,
            "username": "updated_user",
            "role": "manager",
            "email": "update@example.com",
            "password": "password123"  # include password
        }
        response, status_code = self.user_manager.edit_user(updated_data)
        self.assertEqual(status_code, 200)
        self.assertEqual(response["message"], "User with ID 0 updated successfully")
        self.assertEqual(self.user_manager.users[0]["username"], "updated_user")
        self.assertEqual(self.user_manager.users[0]["role"], "manager")

        # Test editing a non-existent user
        invalid_data = {
            "id": 99,
            "username": "nonexistent",
            "role": "employee",
            "email": "none@example.com",
            "password": "password123"  # Add this line
        }
        response, status_code = self.user_manager.edit_user(invalid_data)
        self.assertEqual(status_code, 404)
        self.assertEqual(response["error"], "User not found")

    def test_login(self):
        # Add a user first
        data = {"username": "test_user", "password": "password123", "role": "employee", "email": "test@example.com"}
        self.user_manager.add_user(data)

        # Test successful login
        response, status_code = self.user_manager.login("test_user", "password123")
        self.assertEqual(status_code, 200)
        self.assertTrue("token" in response)
        self.assertEqual(response["role"], "employee")

        # Test failed login
        response, status_code = self.user_manager.login("test_user", "wrongpassword")
        self.assertEqual(status_code, 401)
        self.assertEqual(response["error"], "Invalid credentials")

if __name__ == "__main__":
    unittest.main()
