# Day-2-Day

A Flask-based task management and calendar application for students to track assignments, deadlines, and coursework.

## Overview

Day-2-Day helps students stay organized by integrating with Canvas LMS to track assignments, providing notifications for upcoming deadlines, and offering tools to manage notes and tasks efficiently.

## Features

### ✅ Implemented 
- **Task Management**: View and filter assignments by course, priority, status, and due date
- **Smart Notifications**: Get alerts for overdue, due today, and upcoming tasks
- **Notes System**: Add, edit, delete, and search notes for assignments
- **Email Notifications** (skeleton): Email alerts for overdue, due today, and upcoming tasks
- **Calendar View**: Interactive calendar grid for visualizing assignments
- **Dashboard**: Unified view with assignments, notes, and notifications

### 🚧 In Progress
- **Canvas API Integration**: Automatic assignment syncing from Canvas LMS
- **User Authentication**: Login/logout with Canvas OAuth
- **Admin Profile Management**: User and profile management system

## Tech Stack

- **Backend**: Python 3.10+, Flask
- **Frontend**: Jinja2 templates, HTML/CSS, JavaScript
- **Testing**: unittest
- **Version Control**: Git, GitHub


## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/evodolaz/project-day-2-day.git
   cd project-day-2-day
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   cd backend/src
   py -m calendar_app.app
   ```

4. **Open in browser:**
   ```
   http://localhost:5000
   ```

### Running Tests

```bash
# Run all tests
python -m unittest discover -s backend/tests -v

# Run specific test file
python -m unittest backend.tests.test_date_utils
```


## Development

### Team Workflow
1. Create a new branch for each feature
2. Make changes and commit frequently
3. Push branch and create a Pull Request
4. Get at least 1 approval before merging
5. Squash and merge to keep history clean

See [docs/contributing.md](docs/contributing.md) for detailed guidelines on:
- AI usage policy
- Code review process
- Development tools
- Coding standards

### Import Style
All imports use the `calendar_app` prefix:
```python
from calendar_app.logic.NoteManager import NoteManager
from calendar_app.utils.date_utils import format_date
```

Run the app from `backend/src/` directory.

## API Endpoints

### Main Routes
- `GET /` - Dashboard
- `GET /calendar` - Calendar view

### Notes Routes
- `POST /add-note` - Create a note
- `POST /edit-note/<id>` - Update a note
- `GET /delete-note/<id>` - Delete a note

### Task Routes
- `GET /tasks/` - Filter tasks with query parameters
- `GET /tasks/overdue` - Get overdue tasks
- `GET /tasks/due-soon` - Get tasks due within 7 days
- `GET /tasks/today` - Get tasks due today
- `GET /tasks/stats` - Get task statistics


### Team Members
- Laken Hollen
- Evan Knieriem
- Lucia Martinez-Segundo
- Evgeniy Vodolazov

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built for C346 Software Engineering course
- Canvas API integration planned
- Special thanks to our instructors and peers