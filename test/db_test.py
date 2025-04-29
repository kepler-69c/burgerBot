import unittest
from helpers.db import *


class DBTest(unittest.TestCase):
    def test_add_email(self):
        token = add_email("mail@example.com", "always")
        self.assertIsNotNone(token)
        self.assertEqual(get_email(token)["email"], "mail@example.com")

    def test_update_settings(self):
        token = add_email("mail@example.com", "always")
        update_settings(token, "never")
        self.assertEqual(get_email(token)["sending"], "never")

    def test_get_emails(self):
        add_email("mail@example.com", "always")
        self.assertGreaterEqual(len(get_emails()), 1)

    def test_delete_email(self):
        token = add_email("mail@example.com", "always")
        delete_email(token)
        self.assertIsNone(get_email(token))


if __name__ == "__main__":
    unittest.main()
