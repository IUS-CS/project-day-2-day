import sys
import os
import unittest

# Fix import path to find utils module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.validators import validate_task_name, validate_priority, validate_email


class TestValidateTaskName(unittest.TestCase):
    """Test cases for validate_task_name function."""

    def test_valid_task_name(self):
        self.assertTrue(validate_task_name("Complete homework"))

    def test_empty_string(self):
        self.assertFalse(validate_task_name(""))

    def test_whitespace_only(self):
        self.assertFalse(validate_task_name("   "))

    def test_too_long(self):
        self.assertFalse(validate_task_name("a" * 201))

    def test_exactly_200_chars(self):
        self.assertTrue(validate_task_name("a" * 200))


class TestValidatePriority(unittest.TestCase):
    """Test cases for validate_priority function."""

    def test_valid_priorities(self):
        self.assertTrue(validate_priority("high"))
        self.assertTrue(validate_priority("medium"))
        self.assertTrue(validate_priority("low"))

    def test_case_insensitive(self):
        self.assertTrue(validate_priority("HIGH"))
        self.assertTrue(validate_priority("Medium"))

    def test_invalid_priority(self):
        self.assertFalse(validate_priority("urgent"))


class TestValidateEmail(unittest.TestCase):
    """Test cases for validate_email function."""

    def test_valid_emails(self):
        self.assertTrue(validate_email("test@example.com"))
        self.assertTrue(validate_email("user.name@domain.co.uk"))

    def test_invalid_emails(self):
        self.assertFalse(validate_email("notanemail.com"))
        self.assertFalse(validate_email("test@"))
        self.assertFalse(validate_email(""))


if __name__ == '__main__':
    unittest.main()