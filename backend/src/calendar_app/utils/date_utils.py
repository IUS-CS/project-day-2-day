from datetime import datetime, date, timedelta
from typing import Optional


def format_date(date_obj: datetime | date, format_type: str = "short") -> str:
    """
    Format a date object for display.

    Args:
        date_obj: datetime or date object to format
        format_type: "short" (MM/DD/YYYY) or "long" (Month DD, YYYY)

    """
    if format_type == "long":
        return date_obj.strftime("%B %d, %Y")
    return date_obj.strftime("%m/%d/%Y")


def is_overdue(due_date: datetime | date) -> bool:
    """
    Check if a task is overdue.

    Args:
        due_date: The task's due date

    Returns:
        True if the date is in the past, False otherwise

    """
    if isinstance(due_date, datetime):
        due_date = due_date.date()

    return due_date < date.today()


def days_until(target_date: datetime | date) -> int:
    """
    Calculate the number of days until a target date.

    Args:
        target_date: The target date

    Returns:
        Number of days (negative if in the past)

    """
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    return (target_date - date.today()).days


def parse_date(date_string: str) -> Optional[datetime]:
    """
    Parse a date string in YYYY-MM-DD format.

    Args:
        date_string: String representation of a date (YYYY-MM-DD)

    Returns:
        datetime object or None if parsing fails

    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None