from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, timedelta
from calendar_app.logic.TaskFilter import TaskFilter

# Create blueprint
task_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Sample tasks (will be replaced with real Canvas API data)
SAMPLE_TASKS = [
    {
        'id': 1,
        'name': 'C346 Project Proposal',
        'due_date': datetime.now() - timedelta(days=3),
        'status': 'in_progress',
        'priority': 'high',
        'course_id': 101,
        'course_name': 'Software Engineering',
        'description': 'Submit project proposal document'
    },
    {
        'id': 2,
        'name': 'Canvas API Research',
        'due_date': datetime.now() + timedelta(days=2),
        'status': 'not_started',
        'priority': 'high',
        'course_id': 101,
        'course_name': 'Software Engineering',
        'description': 'Research Canvas LMS API documentation'
    },
    {
        'id': 3,
        'name': 'Database Assignment',
        'due_date': datetime.now() + timedelta(days=5),
        'status': 'in_progress',
        'priority': 'medium',
        'course_id': 102,
        'course_name': 'Database Systems',
        'description': 'Complete SQL queries homework'
    },
    {
        'id': 4,
        'name': 'Algorithm Problem Set',
        'due_date': datetime.now() + timedelta(days=1),
        'status': 'not_started',
        'priority': 'high',
        'course_id': 103,
        'course_name': 'Algorithms',
        'description': 'Solve dynamic programming problems'
    },
    {
        'id': 5,
        'name': 'Reading Quiz',
        'due_date': datetime.now(),
        'status': 'not_started',
        'priority': 'low',
        'course_id': 104,
        'course_name': 'Literature',
        'description': 'Complete online quiz on chapters 5-7'
    },
    {
        'id': 6,
        'name': 'Lab Report',
        'due_date': datetime.now() + timedelta(days=10),
        'status': 'not_started',
        'priority': 'medium',
        'course_id': 105,
        'course_name': 'Physics',
        'description': 'Write lab report for experiment 3'
    }
]


@task_bp.route('/')
def list_tasks():
    """
    List and filter tasks based on query parameters.

    Query Parameters:
        course_id (int): Filter by course ID
        status (str): Filter by status (pending, in_progress, completed)
        priority (str): Filter by priority (high, medium, low)
        filter_type (str): Quick filters (overdue, due_soon, this_week, today)
        sort_by (str): Sort by (due_date, priority, course)
        search (str): Search in task names and descriptions

    Returns:
        JSON response with filtered tasks
    """
    # Get filter parameters
    course_id = request.args.get('course_id', type=int)
    status = request.args.get('status')
    priority = request.args.get('priority')
    filter_type = request.args.get('filter_type')
    sort_by = request.args.get('sort_by', 'due_date')
    search_query = request.args.get('search', '')

    # Create filter
    task_filter = TaskFilter(SAMPLE_TASKS)

    # Apply search first if provided
    if search_query:
        task_filter.search(search_query)

    # Apply quick filters
    if filter_type == 'overdue':
        results = task_filter.filter_overdue().sort_by_due_date().get_results()
    elif filter_type == 'due_soon':
        results = task_filter.filter_due_soon(days=7).sort_by_due_date().get_results()
    elif filter_type == 'this_week':
        results = task_filter.get_this_week()
    elif filter_type == 'today':
        results = task_filter.get_today()
    else:
        # Apply individual filters
        if course_id:
            task_filter.filter_by_course(course_id)

        if status:
            task_filter.filter_by_status(status)

        if priority:
            task_filter.filter_by_priority(priority)

        # Apply sorting
        if sort_by == 'due_date':
            task_filter.sort_by_due_date()
        elif sort_by == 'priority':
            task_filter.sort_by_priority()
        elif sort_by == 'course':
            task_filter.sort_by_course()

        results = task_filter.get_results()

    # Return JSON response
    return jsonify({
        'tasks': results,
        'count': len(results),
        'filters': {
            'course_id': course_id,
            'status': status,
            'priority': priority,
            'filter_type': filter_type,
            'sort_by': sort_by,
            'search': search_query
        }
    })


@task_bp.route('/by-course/<int:course_id>')
def tasks_by_course(course_id):
    """
    Get all tasks for a specific course.

    Args:
        course_id: ID of the course

    Returns:
        JSON response with tasks for the course
    """
    task_filter = TaskFilter(SAMPLE_TASKS)
    results = task_filter.get_by_course_sorted(course_id)

    return jsonify({
        'course_id': course_id,
        'tasks': results,
        'count': len(results)
    })


@task_bp.route('/overdue')
def overdue_tasks():
    """Get all overdue tasks."""
    task_filter = TaskFilter(SAMPLE_TASKS)
    results = task_filter.filter_overdue().sort_by_due_date().get_results()

    return jsonify({
        'tasks': results,
        'count': len(results)
    })


@task_bp.route('/due-soon')
def due_soon_tasks():
    """
    Get tasks due soon.

    Query Parameters:
        days (int): Number of days to look ahead (default: 7)
    """
    days = request.args.get('days', 7, type=int)

    task_filter = TaskFilter(SAMPLE_TASKS)
    results = task_filter.filter_due_soon(days=days).sort_by_due_date().get_results()

    return jsonify({
        'tasks': results,
        'count': len(results),
        'days_ahead': days
    })


@task_bp.route('/today')
def today_tasks():
    """Get tasks due today."""
    task_filter = TaskFilter(SAMPLE_TASKS)
    results = task_filter.get_today()

    return jsonify({
        'tasks': results,
        'count': len(results)
    })


@task_bp.route('/this-week')
def this_week_tasks():
    """Get tasks due this week."""
    task_filter = TaskFilter(SAMPLE_TASKS)
    results = task_filter.get_this_week()

    return jsonify({
        'tasks': results,
        'count': len(results)
    })


@task_bp.route('/courses')
def list_courses():
    """
    Get list of unique courses from tasks.

    Returns:
        JSON response with course list
    """
    # Extract unique courses
    courses = {}
    for task in SAMPLE_TASKS:
        course_id = task.get('course_id')
        if course_id and course_id not in courses:
            courses[course_id] = {
                'id': course_id,
                'name': task.get('course_name'),
                'task_count': 0
            }

    # Count tasks per course
    for task in SAMPLE_TASKS:
        course_id = task.get('course_id')
        if course_id in courses:
            courses[course_id]['task_count'] += 1

    return jsonify({
        'courses': list(courses.values()),
        'count': len(courses)
    })


@task_bp.route('/stats')
def task_stats():
    """
    Get statistics about tasks.

    Returns:
        JSON response with task statistics
    """
    task_filter = TaskFilter(SAMPLE_TASKS)

    stats = {
        'total': len(SAMPLE_TASKS),
        'overdue': task_filter.reset().filter_overdue().count(),
        'due_today': len(task_filter.reset().get_today()),
        'due_this_week': len(task_filter.reset().get_this_week()),
        'due_soon': task_filter.reset().filter_due_soon(7).count(),
        'by_priority': {
            'high': task_filter.reset().filter_by_priority('high').count(),
            'medium': task_filter.reset().filter_by_priority('medium').count(),
            'low': task_filter.reset().filter_by_priority('low').count()
        },
        'by_status': {
            'not_started': task_filter.reset().filter_by_status('not_started').count(),
            'in_progress': task_filter.reset().filter_by_status('in_progress').count(),
            'completed': task_filter.reset().filter_by_status('completed').count()
        }
    }

    return jsonify(stats)


# Helper function to get task_filter instance (for use in other blueprints)
def get_sample_tasks():
    """Get the sample tasks list."""
    return SAMPLE_TASKS