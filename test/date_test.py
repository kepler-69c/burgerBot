import datetime
import unittest
from helpers.datehandler import is_quiet_date


class DateTest(unittest.TestCase):
    def test_is_quiet_date(self):
        self.assertTrue(is_quiet_date(datetime.date(2024, 12, 25), ["20241225"]))

    def test_is_quiet_range(self):
        self.assertTrue(is_quiet_date(datetime.date(2024, 12, 26), ["20241225/20241227"]))

    def test_is_not_quiet_range(self):
        self.assertFalse(is_quiet_date(datetime.date(2024, 12, 28), ["20241225/20241227"]))

    def test_is_complex_range(self):
        self.assertTrue(is_quiet_date(datetime.date(2024, 12, 25), ["20241225", "20240101/20240102"]))

    def test_is_invalid_date(self):
        with self.assertRaises(ValueError):
            is_quiet_date(datetime.date(2024, 12, 25), ["invalid_date"])


if __name__ == '__main__':
    unittest.main()
