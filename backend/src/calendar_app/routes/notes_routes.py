from flask import Blueprint, request, redirect, url_for
from backend.src.calendar_app.logic.NoteManager import NoteManager

# Create blueprint
notes_bp = Blueprint('notes', __name__)

# Initialize note manager
note_manager = NoteManager()

# Add some sample notes
note_manager.create_note(task_id=1, content="Review formatting before submission.")
note_manager.create_note(task_id=1, content="Confirm authentication method for Canvas API.")
note_manager.create_note(task_id=2, content="Research Flask blueprints for better organization.")


@notes_bp.route("/add-note", methods=["POST"])
def add_note():
    """Add a new note to a task."""
    content = request.form.get("content")
    task_id = request.form.get("task_id", 1, type=int)

    if content:
        note_manager.create_note(task_id=task_id, content=content)

    return redirect(url_for("main.index"))


@notes_bp.route("/edit-note/<int:note_id>", methods=["POST"])
def edit_note(note_id):
    """Edit an existing note."""
    new_content = request.form.get("content")

    if new_content:
        note_manager.update_note(note_id, new_content)

    return redirect(url_for("main.index"))


@notes_bp.route("/delete-note/<int:note_id>")
def delete_note(note_id):
    """Delete a note."""
    note_manager.delete_note(note_id)
    return redirect(url_for("main.index"))


# Helper function to get note_manager instance
def get_note_manager():
    """Get the note manager instance."""
    return note_manager