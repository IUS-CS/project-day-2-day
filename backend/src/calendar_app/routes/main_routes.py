"""
Blueprint for main page routes (dashboard, calendar).
"""

from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime, timedelta

from calendar_app.logic.Notifications import Notifications
from calendar_app.routes.notes_routes import note_manager
from calendar_app.logic.TaskFilter import TaskFilter
from calendar_app.data.task_completion_repo import TaskCompletionRepo
from calendar_app.data.db import init_db
#Create blueprint
main_bp = Blueprint('main', __name__)

SessionFactory = init_db()
task_completion_repo = TaskCompletionRepo(SessionFactory)
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

    # Get notes based on filters
    if note_task_filter:
        notes = note_manager.get_notes_for_task(note_task_filter)
    elif search_query:
        notes = note_manager.search_notes(search_query)
    else:
        notes = note_manager.get_all_notes()

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

    # Get notifications for all tasks (not filtered)
    notifications = notification_service.get_notifications_for_tasks(SAMPLE_TASKS)
    notification_counts = notification_service.count_notifications(SAMPLE_TASKS)

    # Get completion stats
    completion_stats = task_completion_repo.get_stats([task["id"] for task in SAMPLE_TASKS])

    return render_template("index.html",
                           notes=notes,
                           tasks=filtered_tasks,
                           all_tasks=task_completion_repo.add_completion_status_to_tasks(SAMPLE_TASKS),  # For note task selection
                           courses=courses,
                           notifications=notifications,
                           notification_counts=notification_counts,
                           completion_stats=completion_stats,
                           current_filter=note_task_filter,
                           search_query=search_query,
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


@main_bp.route("/calendar")
def calendar_view():
    """Calendar page."""
    return render_template("calendar.html")