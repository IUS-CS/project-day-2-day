import re


def validate_task_name(name: str) -> bool:
    """
    Validate a task name.

    Args:
        name: The task name to validate

    Returns:
        True if valid, False otherwise

    Rules:
        - Not empty or only whitespace
        - Between 1 and 200 characters

    """
    if not name or not isinstance(name, str):
        return False

    name = name.strip()
    return 1 <= len(name) <= 200


def validate_priority(priority: str) -> bool:
    """
    Validate task priority value.

    Args:
        priority: Priority as string ("high", "medium", "low")

    Returns:
        True if valid, False otherwise

    """
    valid_priorities = ["high", "medium", "low"]

    if not isinstance(priority, str):
        return False

    return priority.lower() in valid_priorities


def validate_email(email: str) -> bool:
    """
    Validate an email address format.

    Args:
        email: Email address to validate

    Returns:
        True if format is valid, False otherwise

    """
    if not email or not isinstance(email, str):
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_note_content(content: str) -> bool:
    """
    Validate note content.

    Args:
        content: Note content to validate

    Returns:
        True if valid, False otherwise

    Rules:
        - Not empty or only whitespace
        - Maximum 5000 characters

    """
    if not content or not isinstance(content, str):
        return False

    content = content.strip()
    return 1 <= len(content) <= 5000
