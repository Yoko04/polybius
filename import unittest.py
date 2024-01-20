import unittest
import os
from polybius import DatabaseManager, PolybiusCipher

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Set up a test database
        self.test_db_name = "test_users.db"
        self.db_manager = DatabaseManager(self.test_db_name)

    def tearDown(self):
        # Clean up the test database
        self.db_manager.db.close()
        os.remove(self.test_db_name)

    def test_register_user(self):
        # Test if the user is correctly registered and data is inserted into the database
        username = "test_user"
        password = "test_password"
        self.assertFalse(self.db_manager.check_user_exists(username))

        # Register the user
        self.db_manager.register_user(username, password)

        # Check if the user exists after registration
        self.assertTrue(self.db_manager.check_user_exists(username))

    def test_login_user(self):
        # Test if the login functionality works correctly
        username = "test_user"
        password = "test_password"

        # Register the user
        self.db_manager.register_user(username, password)

        # Check if the login is successful with correct credentials
        self.assertTrue(self.db_manager.login_user(username, password))

        # Check if the login fails with incorrect password
        self.assertFalse(self.db_manager.login_user(username, "wrong_password"))

        # Check if the login fails with incorrect username
        self.assertFalse(self.db_manager.login_user("wrong_username", password))

class TestPolybiusCipher(unittest.TestCase):
    def setUp(self):
        self.cipher_manager = PolybiusCipher()

    def test_polybius_cipher(self):
        text = "HELLO"
        expected_result = "2315313134"
        result = self.cipher_manager.polybius_cipher(text, self.cipher_manager.polybius_table_en)
        self.assertEqual(result, expected_result)

    def test_polybius_decipher(self):
        text = "2315313134"
        expected_result = "HELLO"
        result = self.cipher_manager.polybius_decipher(text, self.cipher_manager.polybius_table_en)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()
