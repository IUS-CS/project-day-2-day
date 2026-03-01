from typing import List, Dict
from datetime import datetime, date
from backend.src.calendar_app.utils.date_utils import is_overdue, days_until, format_date


class Notifications:
    """
    Generates notifications for tasks based on due dates.

    Uses date utilities to determine task urgency and create
    appropriate notifications for users.
    """

    def __init__(self, due_soon_threshold: int = 3):
        """
        Initialize the NotificationService.

        Args:
            due_soon_threshold: Number of days to consider a task "due soon" (default: 3)
        """
        self.due_soon_threshold = due_soon_threshold

    def get_notifications_for_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        Generate all notifications for a list of tasks.

        Args:
            tasks: List of task dictionaries with 'id', 'name', 'due_date'

        Returns:
            List of notification dictionaries with 'type', 'message', 'task', 'priority'
        """
        notifications = []

        for task in tasks:
            task_notifications = self._get_notifications_for_task(task)
            notifications.extend(task_notifications)

        # Sort by priority
        notifications.sort(key=lambda n: n['priority'])

        return notifications

    def _get_notifications_for_task(self, task: Dict) -> List[Dict]:
        """
        Generate notifications for a single task.

        Args:
            task: Task dictionary with 'id', 'name', 'due_date'

        Returns:
            List of notifications for this task
        """
        notifications = []
        due_date = task['due_date']

        # Skip if no due date
        if not due_date:
            return notifications

        # Check if overdue
        if is_overdue(due_date):
            days_overdue = abs(days_until(due_date))
            notifications.append({
                'type': 'overdue',
                'message': f"'{task['name']}' is {days_overdue} day(s) overdue!",
                'task': task,
                'priority': 1,  # Highest priority
                'icon': '🔴',
                'color': '#dc3545'  # Red
            })

        # Check if due today
        elif days_until(due_date) == 0:
            notifications.append({
                'type': 'due_today',
                'message': f"'{task['name']}' is due today!",
                'task': task,
                'priority': 2,
                'icon': '⚠️',
                'color': '#ffc107'  # Yellow
            })

        # Check if due soon
        elif 0 < days_until(due_date) <= self.due_soon_threshold:
            days_remaining = days_until(due_date)
            notifications.append({
                'type': 'due_soon',
                'message': f"'{task['name']}' is due in {days_remaining} day(s)",
                'task': task,
                'priority': 3,
                'icon': '🔔',
                'color': '#28a745'  # Green
            })

        return notifications

    def get_overdue_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        Get only overdue tasks.

        Args:
            tasks: List of task dictionaries

        Returns:
            List of overdue tasks
        """
        return [task for task in tasks if task.get('due_date') and is_overdue(task['due_date'])]

    def get_due_soon_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        Get tasks due soon

        Args:
            tasks: List of task dictionaries

        Returns:
            List of tasks due soon
        """
        return [task for task in tasks
                if task.get('due_date')
                and 0 < days_until(task['due_date']) <= self.due_soon_threshold]

    def get_due_today_tasks(self, tasks: List[Dict]) -> List[Dict]:
        """
        Get tasks due today.

        Args:
            tasks: List of task dictionaries

        Returns:
            List of tasks due today
        """
        return [task for task in tasks
                if task.get('due_date')
                and days_until(task['due_date']) == 0]

    def count_notifications(self, tasks: List[Dict]) -> Dict[str, int]:
        """
        Count notifications by type.

        Args:
            tasks: List of task dictionaries

        Returns:
            Dictionary with counts: {'overdue': 2, 'due_today': 1, 'due_soon': 3}
        """
        return {
            'overdue': len(self.get_overdue_tasks(tasks)),
            'due_today': len(self.get_due_today_tasks(tasks)),
            'due_soon': len(self.get_due_soon_tasks(tasks))
        }

    def has_urgent_notifications(self, tasks: List[Dict]) -> bool:
        """
        Check if there are any urgent notifications (overdue or due today).

        Args:
            tasks: List of task dictionaries

        Returns:
            True if there are overdue or due today tasks
        """
        return len(self.get_overdue_tasks(tasks)) > 0 or len(self.get_due_today_tasks(tasks)) > 0