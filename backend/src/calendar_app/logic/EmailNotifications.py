#Currently a skeleton/framework

from typing import List, Dict, Optional
from datetime import datetime
from calendar_app.utils.date_utils import format_date, days_until


class EmailNotifications:
    """
    Handles email notifications for task reminders.
    """

    def __init__(self, smtp_config: Optional[Dict] = None):
        self.smtp_config = smtp_config or {}
        self.enabled = self._check_email_enabled()

    def _check_email_enabled(self) -> bool:
        required_keys = ['host', 'port', 'username', 'password', 'from_email']
        return all(key in self.smtp_config for key in required_keys)

    def send_due_soon_notification(self, user_email: str, tasks: List[Dict]) -> bool:
        """
        Send notification for tasks due soon.

        Args:
            user_email: User's email address
            tasks: List of tasks due soon

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            print(f"[EMAIL SKELETON] Would send 'due soon' notification to {user_email}")
            print(f"[EMAIL SKELETON] Tasks: {len(tasks)} tasks due soon")
            return True

        subject = f"You have {len(tasks)} task(s) due soon"
        body = self._generate_due_soon_email_body(tasks)

        return self._send_email(user_email, subject, body)

    def send_overdue_notification(self, user_email: str, tasks: List[Dict]) -> bool:
        """
        Send notification for overdue tasks.

        Args:
            user_email: User's email address
            tasks: List of overdue tasks

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            print(f"[EMAIL SKELETON] Would send 'overdue' notification to {user_email}")
            print(f"[EMAIL SKELETON] Tasks: {len(tasks)} overdue tasks")
            return True

        subject = f"⚠️ You have {len(tasks)} overdue task(s)"
        body = self._generate_overdue_email_body(tasks)

        return self._send_email(user_email, subject, body)

    def send_daily_digest(self, user_email: str, tasks_today: List[Dict],
                          tasks_upcoming: List[Dict]) -> bool:
        """
        Send daily digest email with today's and upcoming tasks.

        Args:
            user_email: User's email address
            tasks_today: Tasks due today
            tasks_upcoming: Tasks due in the next few days

        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            print(f"[EMAIL SKELETON] Would send daily digest to {user_email}")
            print(f"[EMAIL SKELETON] Today: {len(tasks_today)}, Upcoming: {len(tasks_upcoming)}")
            return True

        subject = f"Daily Task Digest - {datetime.now().strftime('%B %d, %Y')}"
        body = self._generate_daily_digest_body(tasks_today, tasks_upcoming)

        return self._send_email(user_email, subject, body)

    def _generate_due_soon_email_body(self, tasks: List[Dict]) -> str:
        """Generate email body for due soon notifications."""
        body = "Hello,\n\n"
        body += "The following tasks are due soon:\n\n"

        for task in tasks:
            due_date = task.get('due_date')
            days_left = days_until(due_date) if due_date else 0

            body += f"• {task.get('name', 'Unnamed Task')}\n"
            body += f"  Due: {format_date(due_date, 'long')} ({days_left} day(s) remaining)\n"
            body += f"  Course: {task.get('course_name', 'Unknown')}\n\n"

        body += "\nStay on track!\n"
        body += "- Day-2-Day Team"

        return body

    def _generate_overdue_email_body(self, tasks: List[Dict]) -> str:
        """Generate email body for overdue notifications."""
        body = "Hello,\n\n"
        body += "⚠️ The following tasks are overdue:\n\n"

        for task in tasks:
            due_date = task.get('due_date')
            days_overdue = abs(days_until(due_date)) if due_date else 0

            body += f"• {task.get('name', 'Unnamed Task')}\n"
            body += f"  Was due: {format_date(due_date, 'long')} ({days_overdue} day(s) ago)\n"
            body += f"  Course: {task.get('course_name', 'Unknown')}\n\n"

        body += "\nDon't worry, you can still catch up!\n"
        body += "- Day-2-Day Team"

        return body

    def _generate_daily_digest_body(self, tasks_today: List[Dict],
                                    tasks_upcoming: List[Dict]) -> str:
        """Generate email body for daily digest."""
        body = f"Good morning!\n\n"
        body += f"Here's your task summary for {datetime.now().strftime('%B %d, %Y')}:\n\n"

        # Today's tasks
        body += f"📅 DUE TODAY ({len(tasks_today)}):\n"
        if tasks_today:
            for task in tasks_today:
                body += f"• {task.get('name', 'Unnamed Task')}\n"
        else:
            body += "No tasks due today! 🎉\n"

        body += "\n"

        # Upcoming tasks
        body += f"🔔 COMING UP ({len(tasks_upcoming)}):\n"
        if tasks_upcoming:
            for task in tasks_upcoming:
                due_date = task.get('due_date')
                days_left = days_until(due_date) if due_date else 0
                body += f"• {task.get('name', 'Unnamed Task')} - {days_left} day(s)\n"
        else:
            body += "No upcoming tasks!\n"

        body += "\nHave a productive day!\n"
        body += "- Day-2-Day Team"

        return body

    def _send_email(self, to_email: str, subject: str, body: str) -> bool:

        # TODO: Implement actual email sending when SMTP is configured

        print(f"\n[EMAIL SKELETON] Email Details:")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}\n")

        return True

    def get_notification_preview(self, notification_type: str,
                                 tasks: List[Dict]) -> Dict[str, str]:
        """
        Get a preview of what an email notification would look like.

        Args:
            notification_type: Type of notification ('due_soon', 'overdue', 'daily_digest')
            tasks: List of tasks

        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        if notification_type == 'due_soon':
            subject = f"You have {len(tasks)} task(s) due soon"
            body = self._generate_due_soon_email_body(tasks)
        elif notification_type == 'overdue':
            subject = f"⚠️ You have {len(tasks)} overdue task(s)"
            body = self._generate_overdue_email_body(tasks)
        elif notification_type == 'daily_digest':
            tasks_today = [t for t in tasks if days_until(t.get('due_date')) == 0]
            tasks_upcoming = [t for t in tasks if 0 < days_until(t.get('due_date', datetime.max)) <= 7]
            subject = f"Daily Task Digest - {datetime.now().strftime('%B %d, %Y')}"
            body = self._generate_daily_digest_body(tasks_today, tasks_upcoming)
        else:
            subject = "Unknown notification type"
            body = ""

        return {'subject': subject, 'body': body}