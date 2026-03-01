from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from backend.src.calendar_app.logic.Notifications import Notifications
from backend.src.calendar_app.routes.notes_routes import get_note_manager

# Create blueprint
main_bp = Blueprint('main', __name__)

# Initialize notification service
notification_service = Notifications(due_soon_threshold=3)

# Sample tasks with due dates
SAMPLE_TASKS = [
    {
        'id': 1,
        'name': 'C346 Proposal',
        'due_date': datetime.now() - timedelta(days=2),  # Overdue
        'status': 'In Progress'
    },
    {
        'id': 2,
        'name': 'Canvas API Research',
        'due_date': datetime.now() + timedelta(days=1),  # Due soon
        'status': 'Not Started'
    },
    {
        'id': 3,
        'name': 'Project Sprint 2',
        'due_date': datetime.now(),  # Due today
        'status': 'In Progress'
    }
]


@main_bp.route("/")
def index():
    """Dashboard home page with notes and notifications."""
    # Get note manager from notes blueprint
    note_manager = get_note_manager()

    # Get filter and search parameters
    task_filter = request.args.get("task_id", type=int)
    search_query = request.args.get("search", "")

    # Get notes based on filters
    if task_filter:
        notes = note_manager.get_notes_for_task(task_filter)
    elif search_query:
        notes = note_manager.search_notes(search_query)
    else:
        notes = note_manager.get_all_notes()

    # Get notifications for tasks
    notifications = notification_service.get_notifications_for_tasks(SAMPLE_TASKS)
    notification_counts = notification_service.count_notifications(SAMPLE_TASKS)

    return render_template("index.html",
                           notes=notes,
                           tasks=SAMPLE_TASKS,
                           notifications=notifications,
                           notification_counts=notification_counts,
                           current_filter=task_filter,
                           search_query=search_query)


@main_bp.route("/calendar")
def calendar_view():
    """Calendar page."""
    return render_template("calendar.html")