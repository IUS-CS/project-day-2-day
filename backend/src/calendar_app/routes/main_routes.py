"""
Blueprint for main page routes (dashboard, calendar).
"""

from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from calendar_app.logic.Notifications import Notifications

# FIX: import the shared note_manager instance instead of get_note_manager
from calendar_app.routes.notes_routes import note_manager
from calendar_app.logic.TaskFilter import TaskFilter
from calendar_app.routes.notes_routes import get_note_manager

# Create blueprint
main_bp = Blueprint('main', __name__)

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
    """Dashboard home page with notes and notifications."""
    """Dashboard home page with notes, tasks, and notifications."""
    # Get note manager from notes blueprint
    note_manager = get_note_manager()

    # Get note filter parameters
    note_task_filter = request.args.get("task_id", type=int)
    search_query = request.args.get("search", "")

    # Get notes based on filters
    if note_task_filter:
        notes = note_manager.get_notes_for_task(note_task_filter)
    elif search_query:
        notes = note_manager.search_notes(search_query)
    else:
        notes = note_manager.get_all_notes()

    # Notifications
    notifications = notification_service.get_notifications_for_tasks(SAMPLE_TASKS)
    notification_counts = notification_service.count_notifications(SAMPLE_TASKS)

    return render_template(
        "index.html",
        notes=notes,
        tasks=SAMPLE_TASKS,
        notifications=notifications,
        notification_counts=notification_counts,
        current_filter=task_filter,
        search_query=search_query
    )
    # Get task filter parameters
    task_course_filter = request.args.get("course_id", type=int)
    task_status_filter = request.args.get("status")
    task_priority_filter = request.args.get("priority")
    task_quick_filter = request.args.get("task_filter")  # 'overdue', 'due_soon', 'today'

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

    # Get all unique courses for filter dropdown
    courses = {}
    for task in SAMPLE_TASKS:
        course_id = task.get('course_id')
        if course_id and course_id not in courses:
            courses[course_id] = task.get('course_name')

    # Get notifications for all tasks (not filtered)
    notifications = notification_service.get_notifications_for_tasks(SAMPLE_TASKS)
    notification_counts = notification_service.count_notifications(SAMPLE_TASKS)

    return render_template("index.html",
                           notes=notes,
                           tasks=filtered_tasks,
                           all_tasks=SAMPLE_TASKS,  # For note task selection
                           courses=courses,
                           notifications=notifications,
                           notification_counts=notification_counts,
                           current_filter=note_task_filter,
                           search_query=search_query,
                           task_course_filter=task_course_filter,
                           task_status_filter=task_status_filter,
                           task_priority_filter=task_priority_filter,
                           task_quick_filter=task_quick_filter)


@main_bp.route("/calendar")
def calendar_view():
    """Calendar page."""
    return render_template("calendar.html")