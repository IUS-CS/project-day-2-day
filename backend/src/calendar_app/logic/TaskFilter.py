from typing import List, Dict, Optional, Callable
from datetime import datetime, date, timedelta
from calendar_app.utils.date_utils import days_until


class TaskFilter:
    """
    Handles filtering and sorting of tasks/assignments.

    Provides methods to filter tasks by course, date range, status,
    and sort by various criteria.
    """

    def __init__(self, tasks: List[Dict]):
        """
        Initialize TaskFilter with a list of tasks.

        Args:
            tasks: List of task dictionaries
        """
        self.tasks = tasks
        self._filtered_tasks = tasks.copy()

    def filter_by_course(self, course_id: int) -> 'TaskFilter':
        """
        Filter tasks by course/class ID.

        Args:
            course_id: ID of the course to filter by

        Returns:
            Self for method chaining
        """
        self._filtered_tasks = [
            task for task in self._filtered_tasks
            if task.get('course_id') == course_id
        ]
        return self

    def filter_by_status(self, status: str) -> 'TaskFilter':
        """
        Filter tasks by completion status.

        Args:
            status: Status to filter by ('pending', 'in_progress', 'completed', 'cancelled')

        Returns:
            Self for method chaining
        """
        self._filtered_tasks = [
            task for task in self._filtered_tasks
            if task.get('status', '').lower() == status.lower()
        ]
        return self

    def filter_by_date_range(self, start_date: Optional[date] = None,
                             end_date: Optional[date] = None) -> 'TaskFilter':
        """
        Filter tasks by due date range.

        Args:
            start_date: Start of date range (inclusive)
            end_date: End of date range (inclusive)

        Returns:
            Self for method chaining
        """
        filtered = []
        for task in self._filtered_tasks:
            due_date = task.get('due_date')
            if not due_date:
                continue

            # Convert to date if datetime
            if isinstance(due_date, datetime):
                due_date = due_date.date()

            # Check range
            if start_date and due_date < start_date:
                continue
            if end_date and due_date > end_date:
                continue

            filtered.append(task)

        self._filtered_tasks = filtered
        return self

    def filter_overdue(self) -> 'TaskFilter':
        """
        Filter to show only overdue tasks.

        Returns:
            Self for method chaining
        """
        filtered = []
        for task in self._filtered_tasks:
            due_date = task.get('due_date')
            if due_date:
                if isinstance(due_date, datetime):
                    due_date = due_date.date()
                if due_date < date.today():
                    filtered.append(task)

        self._filtered_tasks = filtered
        return self

    def filter_due_soon(self, days: int = 7) -> 'TaskFilter':
        """
        Filter to show tasks due within a certain number of days.

        Args:
            days: Number of days to look ahead (default: 7)

        Returns:
            Self for method chaining
        """
        filtered = []
        for task in self._filtered_tasks:
            due_date = task.get('due_date')
            if due_date:
                days_remaining = days_until(due_date)
                if 0 <= days_remaining <= days:
                    filtered.append(task)

        self._filtered_tasks = filtered
        return self

    def filter_by_priority(self, priority: str) -> 'TaskFilter':
        """
        Filter tasks by priority level.

        Args:
            priority: Priority level ('high', 'medium', 'low')

        Returns:
            Self for method chaining
        """
        self._filtered_tasks = [
            task for task in self._filtered_tasks
            if task.get('priority', '').lower() == priority.lower()
        ]
        return self

    def search(self, query: str) -> 'TaskFilter':
        """
        Search tasks by name/description.

        Args:
            query: Search query string

        Returns:
            Self for method chaining
        """
        if not query:
            return self

        query_lower = query.lower()
        self._filtered_tasks = [
            task for task in self._filtered_tasks
            if query_lower in task.get('name', '').lower() or
               query_lower in task.get('description', '').lower()
        ]
        return self

    def sort_by_due_date(self, reverse: bool = False) -> 'TaskFilter':
        """
        Sort tasks by due date.

        Args:
            reverse: If True, sort newest first (default: False for oldest first)

        Returns:
            Self for method chaining
        """
        self._filtered_tasks.sort(
            key=lambda task: task.get('due_date') or datetime.max,
            reverse=reverse
        )
        return self

    def sort_by_priority(self) -> 'TaskFilter':
        """
        Sort tasks by priority (high → medium → low).

        Returns:
            Self for method chaining
        """
        priority_order = {'high': 1, 'medium': 2, 'low': 3}
        self._filtered_tasks.sort(
            key=lambda task: priority_order.get(task.get('priority', 'low').lower(), 4)
        )
        return self

    def sort_by_course(self) -> 'TaskFilter':
        """
        Sort tasks by course name.

        Returns:
            Self for method chaining
        """
        self._filtered_tasks.sort(
            key=lambda task: task.get('course_name', '')
        )
        return self

    def get_results(self) -> List[Dict]:
        """
        Get the filtered and sorted tasks.

        Returns:
            List of filtered task dictionaries
        """
        return self._filtered_tasks

    def count(self) -> int:
        """
        Get count of filtered tasks.

        Returns:
            Number of tasks after filtering
        """
        return len(self._filtered_tasks)

    def reset(self) -> 'TaskFilter':
        """
        Reset filters to show all tasks.

        Returns:
            Self for method chaining
        """
        self._filtered_tasks = self.tasks.copy()
        return self

    # Convenience methods for common filters

    def get_this_week(self) -> List[Dict]:
        """Get tasks due this week."""
        today = date.today()
        week_end = today + timedelta(days=7)
        return (self.reset()
                .filter_by_date_range(today, week_end)
                .sort_by_due_date()
                .get_results())

    def get_today(self) -> List[Dict]:
        """Get tasks due today."""
        today = date.today()
        return (self.reset()
                .filter_by_date_range(today, today)
                .get_results())

    def get_by_course_sorted(self, course_id: int) -> List[Dict]:
        """Get all tasks for a course, sorted by due date."""
        return (self.reset()
                .filter_by_course(course_id)
                .sort_by_due_date()
                .get_results())