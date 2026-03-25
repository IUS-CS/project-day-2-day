from flask import Blueprint, request, redirect, url_for, render_template
from calendar_app.logic.NoteManager import NoteManager
from calendar_app.data.note_repo import NoteRepo
from calendar_app.data.db import init_db
from flask import Blueprint, request, redirect, url_for
from calendar_app.logic.NoteManager import NoteManager

notes_bp = Blueprint("notes", __name__)

# Initialize DB + repo + manager
SessionFactory = init_db()
note_repo = NoteRepo(SessionFactory)
note_manager = NoteManager(note_repo)


@notes_bp.route("/notes")
def list_notes():
    notes = note_manager.get_all_notes()
    return render_template("notes.html", notes=notes)


@notes_bp.route("/add-note", methods=["POST"])
def add_note():
    content = request.form.get("content", "")
    task_id = int(request.form.get("task_id", 1))
    note_manager.create_note(task_id=task_id, content=content)
    return redirect(url_for("main.index"))


@notes_bp.route("/edit-note/<int:note_id>", methods=["POST"])
def edit_note(note_id):
    new_content = request.form.get("content", "")
    note_manager.update_note(note_id, new_content)
    return redirect(url_for("main.index"))


@notes_bp.route("/delete-note/<int:note_id>")
def delete_note(note_id):
    note_manager.delete_note(note_id)
    return redirect(url_for("main.index"))