"""Unit tests for email_notifications module."""

import sys
import os
import unittest
from datetime import datetime, timedelta

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from calendar_app.logic.EmailNotifications import EmailNotifications
from calendar_app.utils.date_utils import days_until


class TestEmailNotificationService(unittest.TestCase):
    """Test cases for EmailNotificationService."""

    def setUp(self):
        """Set up test fixtures."""
        self.email_service = EmailNotifications()

        # Sample tasks for testing
        self.overdue_task = {
            'id': 1,
            'name': 'Overdue Assignment',
            'due_date': datetime.now() - timedelta(days=3),
            'course_name': 'Software Engineering'
        }

        self.due_soon_task = {
            'id': 2,
            'name': 'Due Soon Task',
            'due_date': datetime.now() + timedelta(days=2),
            'course_name': 'Database Systems'
        }

        self.due_today_task = {
            'id': 3,
            'name': 'Due Today Task',
            'due_date': datetime.now(),
            'course_name': 'Algorithms'
        }

    def test_service_initialization(self):
        """Test that service initializes correctly."""
        self.assertIsNotNone(self.email_service)
        self.assertFalse(self.email_service.enabled)  # No SMTP config

    def test_send_due_soon_notification(self):
        """Test sending due soon notification (skeleton)."""
        tasks = [self.due_soon_task]
        result = self.email_service.send_due_soon_notification('test@example.com', tasks)

        # Should return True even without SMTP (skeleton mode)
        self.assertTrue(result)

    def test_send_overdue_notification(self):
        """Test sending overdue notification (skeleton)."""
        tasks = [self.overdue_task]
        result = self.email_service.send_overdue_notification('test@example.com', tasks)

        self.assertTrue(result)

    def test_send_daily_digest(self):
        """Test sending daily digest (skeleton)."""
        tasks_today = [self.due_today_task]
        tasks_upcoming = [self.due_soon_task]

        result = self.email_service.send_daily_digest(
            'test@example.com',
            tasks_today,
            tasks_upcoming
        )

        self.assertTrue(result)

    def test_generate_due_soon_email_body(self):
        """Test email body generation for due soon notifications."""
        tasks = [self.due_soon_task]
        body = self.email_service._generate_due_soon_email_body(tasks)

        self.assertIn('due soon', body.lower())
        self.assertIn(self.due_soon_task['name'], body)
        self.assertIn(self.due_soon_task['course_name'], body)

    def test_generate_overdue_email_body(self):
        """Test email body generation for overdue notifications."""
        tasks = [self.overdue_task]
        body = self.email_service._generate_overdue_email_body(tasks)

        self.assertIn('overdue', body.lower())
        self.assertIn(self.overdue_task['name'], body)
        self.assertIn(self.overdue_task['course_name'], body)

    def test_generate_daily_digest_body(self):
        """Test email body generation for daily digest."""
        tasks_today = [self.due_today_task]
        tasks_upcoming = [self.due_soon_task]

        body = self.email_service._generate_daily_digest_body(tasks_today, tasks_upcoming)

        self.assertIn('DUE TODAY', body)
        self.assertIn('COMING UP', body)
        self.assertIn(self.due_today_task['name'], body)
        self.assertIn(self.due_soon_task['name'], body)

    def test_get_notification_preview_due_soon(self):
        """Test getting preview for due soon notification."""
        tasks = [self.due_soon_task]
        preview = self.email_service.get_notification_preview('due_soon', tasks)

        self.assertIn('subject', preview)
        self.assertIn('body', preview)
        self.assertIn('due soon', preview['subject'].lower())

    def test_get_notification_preview_overdue(self):
        """Test getting preview for overdue notification."""
        tasks = [self.overdue_task]
        preview = self.email_service.get_notification_preview('overdue', tasks)

        self.assertIn('subject', preview)
        self.assertIn('body', preview)
        self.assertIn('overdue', preview['subject'].lower())

    def test_get_notification_preview_daily_digest(self):
        """Test getting preview for daily digest."""
        tasks = [self.due_today_task, self.due_soon_task]
        preview = self.email_service.get_notification_preview('daily_digest', tasks)

        self.assertIn('subject', preview)
        self.assertIn('body', preview)
        self.assertIn('Daily', preview['subject'])

    def test_email_not_enabled_without_config(self):
        """Test that email is disabled without SMTP configuration."""
        self.assertFalse(self.email_service.enabled)

    def test_email_enabled_with_config(self):
        """Test that email is enabled with proper SMTP configuration."""
        smtp_config = {
            'host': 'smtp.example.com',
            'port': 587,
            'username': 'test@example.com',
            'password': 'password',
            'from_email': 'noreply@example.com'
        }

        service_with_config = EmailNotifications(smtp_config)
        self.assertTrue(service_with_config.enabled)

    def test_multiple_tasks_in_notification(self):
        """Test notification with multiple tasks."""
        tasks = [self.overdue_task, self.due_soon_task, self.due_today_task]
        body = self.email_service._generate_due_soon_email_body(tasks)

        # All tasks should be in the body
        for task in tasks:
            self.assertIn(task['name'], body)


if __name__ == '__main__':
    unittest.main()