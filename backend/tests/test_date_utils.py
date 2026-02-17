import sys
import os
import unittest
from datetime import datetime, date, timedelta

# Fix import path to find utils module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.date_utils import format_date, is_overdue, days_until, parse_date


class TestFormatDate(unittest.TestCase):
    """Test cases for format_date function."""

    def test_format_date_short(self):
        test_date = datetime(2024, 3, 15)
        self.assertEqual(format_date(test_date, "short"), "03/15/2024")

    def test_format_date_long(self):
        test_date = datetime(2024, 3, 15)
        self.assertEqual(format_date(test_date, "long"), "March 15, 2024")

    def test_format_date_default(self):
        test_date = datetime(2024, 3, 15)
        self.assertEqual(format_date(test_date), "03/15/2024")


class TestIsOverdue(unittest.TestCase):
    """Test cases for is_overdue function."""

    def test_overdue_yesterday(self):
        yesterday = date.today() - timedelta(days=1)
        self.assertTrue(is_overdue(yesterday))

    def test_not_overdue_today(self):
        self.assertFalse(is_overdue(date.today()))

    def test_not_overdue_tomorrow(self):
        tomorrow = date.today() + timedelta(days=1)
        self.assertFalse(is_overdue(tomorrow))


class TestDaysUntil(unittest.TestCase):
    """Test cases for days_until function."""

    def test_days_until_tomorrow(self):
        tomorrow = date.today() + timedelta(days=1)
        self.assertEqual(days_until(tomorrow), 1)

    def test_days_until_yesterday(self):
        yesterday = date.today() - timedelta(days=1)
        self.assertEqual(days_until(yesterday), -1)

    def test_days_until_today(self):
        self.assertEqual(days_until(date.today()), 0)


class TestParseDate(unittest.TestCase):
    """Test cases for parse_date function."""

    def test_parse_valid_date(self):
        result = parse_date("2024-03-15")
        self.assertEqual(result, datetime(2024, 3, 15))

    def test_parse_invalid_date(self):
        self.assertIsNone(parse_date("invalid"))

    def test_parse_wrong_format(self):
        self.assertIsNone(parse_date("03/15/2024"))


if __name__ == '__main__':
    unittest.main()