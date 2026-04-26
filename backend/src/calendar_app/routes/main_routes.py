"""
Blueprint for main page routes (dashboard, calendar).
"""

from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, timedelta

from calendar_app.logic.Notifications import Notifications
from calendar_app.routes.notes_routes import note_manager
from calendar_app.logic.TaskFilter import TaskFilter
from calendar_app.data.task_completion_repo import TaskCompletionRepo
from calendar_app.data.custom_notification_repo import CustomNotificationRepo
from calendar_app.data.db import init_db
#Create blueprint
main_bp = Blueprint('main', __name__)

SessionFactory = init_db()
task_completion_repo = TaskCompletionRepo(SessionFactory)
custom_notification_repo = CustomNotificationRepo(SessionFactory)
# Initialize notification service
notification_service = Notifications(due_soon_threshold=3)

# Sample tasks with due dates (will be replaced with Canvas API data)
SAMPLE_TASKS = [
    {
        'id': 1,
        'name': 'C346 Proposal',
        'due_date': datetime.now() - timedelta(days=2),
        'status': 'In Progress',
        'priority': 'high',
        'course_id': 101,
        'course_name': 'Software Engineering'
    },
    {
        'id': 2,
        'name': 'Canvas API Research',
        'due_date': datetime.now() + timedelta(days=1),
        'status': 'Not Started',
        'priority': 'high',
        'course_id': 101,
        'course_name': 'Software Engineering'
    },
    {
        'id': 3,
        'name': 'Project Sprint 2',
        'due_date': datetime.now(),
        'status': 'In Progress',
        'priority': 'medium',
        'course_id': 101,
        'course_name': 'Software Engineering'
    },
    {
        'id': 4,
        'name': 'Database Assignment',
        'due_date': datetime.now() + timedelta(days=5),
        'status': 'Not Started',
        'priority': 'medium',
        'course_id': 102,
        'course_name': 'Database Systems'
    }
]


@main_bp.route("/")
def index():
    """Dashboard home page with notes, tasks, and notifications."""

    # Get note filter parameters
    note_task_filter = request.args.get("task_id", type=int)
    search_query = request.args.get("search", "")
    note_category_filter = request.args.get("note_category", "")
    note_course_filter = request.args.get("note_course_id", type=int)

    # Get notes based on filters
    if note_task_filter:
        notes = note_manager.get_notes_for_task(note_task_filter)
    elif search_query:
        notes = note_manager.search_notes(search_query)
    else:
        notes = note_manager.get_all_notes()

    if note_category_filter:
        notes = [n for n in notes if n.category.lower() == note_category_filter.lower()]

    if note_course_filter:
        task_course_map = {task["id"]: task.get("course_id") for task in SAMPLE_TASKS}
        notes = [n for n in notes if task_course_map.get(n.task_id) == note_course_filter]

    # Get task filter parameters
    task_course_filter = request.args.get("course_id", type=int)
    task_status_filter = request.args.get("status")
    task_priority_filter = request.args.get("priority")
    task_quick_filter = request.args.get("task_filter")  # 'overdue', 'due_soon', 'today'
    show_completed = request.args.get("show_completed", "false") == "true"

    # Apply task filters
    task_filter = TaskFilter(SAMPLE_TASKS)

    if task_quick_filter == 'overdue':
        filtered_tasks = task_filter.filter_overdue().sort_by_due_date().get_results()
    elif task_quick_filter == 'due_soon':
        filtered_tasks = task_filter.filter_due_soon(7).sort_by_due_date().get_results()
    elif task_quick_filter == 'today':
        filtered_tasks = task_filter.get_today()
    else:
        # Apply individual filters
        if task_course_filter:
            task_filter.filter_by_course(task_course_filter)
        if task_status_filter:
            task_filter.filter_by_status(task_status_filter)
        if task_priority_filter:
            task_filter.filter_by_priority(task_priority_filter)

        task_filter.sort_by_due_date()
        filtered_tasks = task_filter.get_results()

    # Add completion status to tasks
    filtered_tasks = task_completion_repo.add_completion_status_to_tasks(filtered_tasks)

    # Filter out completed tasks unless show_completed is true
    if not show_completed:
        filtered_tasks = [t for t in filtered_tasks if not t.get('completed', False)]

    # Get all unique courses for filter dropdown
    courses = {}
    for task in SAMPLE_TASKS:
        course_id = task.get('course_id')
        if course_id and course_id not in courses:
            courses[course_id] = task.get('course_name')

    note_categories = sorted({note.category for note in note_manager.get_all_notes()})

    # Get notifications for all tasks (not filtered), excluding completed ones.
    all_tasks_with_completion = task_completion_repo.add_completion_status_to_tasks(SAMPLE_TASKS)
    notifications = notification_service.get_notifications_for_tasks(all_tasks_with_completion)
    custom_notifications = custom_notification_repo.get_active()
    custom_level_map = {
        "info": {"icon": "📝", "color": "#17a2b8"},
        "warning": {"icon": "⚠️", "color": "#ffc107"},
        "urgent": {"icon": "🚨", "color": "#dc3545"},
    }
    notifications.extend(
        {
            "id": n["id"],
            "type": "custom",
            "message": n["message"],
            "priority": 2 if n["level"] == "urgent" else 4,
            "icon": custom_level_map.get(n["level"], custom_level_map["info"])["icon"],
            "color": custom_level_map.get(n["level"], custom_level_map["info"])["color"],
            "task": {"due_date": datetime.fromisoformat(n["due_date"]) if n.get("due_date") else None},
            "is_custom": True,
            "level": n["level"],
            "created_at": datetime.fromisoformat(n["created_at"]),
        }
        for n in custom_notifications
    )
    notifications.sort(
        key=lambda n: (
            n["priority"],
            n["task"]["due_date"] or datetime.max,
            n.get("created_at", datetime.max),
        )
    )
    notification_counts = notification_service.count_notifications(all_tasks_with_completion)

    # Get completion stats
    completion_stats = task_completion_repo.get_stats([task["id"] for task in SAMPLE_TASKS])

    return render_template("index.html",
                           notes=notes,
                           tasks=filtered_tasks,
                           all_tasks=all_tasks_with_completion,  # For note task selection
                           courses=courses,
                           note_categories=note_categories,
                           notifications=notifications,
                           notification_counts=notification_counts,
                           completion_stats=completion_stats,
                           current_filter=note_task_filter,
                           search_query=search_query,
                           note_category_filter=note_category_filter,
                           note_course_filter=note_course_filter,
                           task_course_filter=task_course_filter,
                           task_status_filter=task_status_filter,
                           task_priority_filter=task_priority_filter,
                           task_quick_filter=task_quick_filter,
                           show_completed=show_completed)


@main_bp.route("/toggle-task/<int:task_id>")
def toggle_task_completion(task_id):
    """Toggle a task's completion status."""
    task_completion_repo.toggle(task_id)
    return redirect(url_for('main.index'))


@main_bp.route("/complete-task/<int:task_id>")
def complete_task(task_id):
    """Mark a task as complete."""
    task_completion_repo.mark_complete(task_id)
    return redirect(url_for('main.index'))


@main_bp.route("/incomplete-task/<int:task_id>")
def incomplete_task(task_id):
    """Mark a task as incomplete."""
    task_completion_repo.mark_incomplete(task_id)
    return redirect(url_for('main.index'))


@main_bp.route("/add-custom-notification", methods=["POST"])
def add_custom_notification():
    """Create a user-defined dashboard notification."""
    message = request.form.get("message", "").strip()
    level = request.form.get("level", "info")
    due_date = request.form.get("due_date", "").strip() or None
    if message:
        custom_notification_repo.create(message=message, level=level, due_date=due_date)
    return redirect(url_for('main.index'))


@main_bp.route("/dismiss-custom-notification/<int:notification_id>")
def dismiss_custom_notification(notification_id):
    """Dismiss a custom notification from the dashboard."""
    custom_notification_repo.dismiss(notification_id)
    return redirect(url_for('main.index'))


@main_bp.route("/calendar")
def calendar_view():
    """Calendar page."""
    return render_template("calendar.html")