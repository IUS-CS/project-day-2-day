# app.py
# This does the initiliazation and execution of the application
# Uses Flask for it all.
# Important note: Serves as the primary backend service for the application
# Delivers frontend pages as well.

from flask import Flask, render_template, request, redirect, url_for
from backend.src.calendar_app.logic.NoteManager import NoteManager

# Initialize note manager
note_manager = NoteManager()

# Add some sample notes for different tasks
# note_manager.create_note(task_id=1, content="Review formatting before submission.")



def create_app():
    app = Flask(__name__)

    # Home route - now with real notes!
    @app.route("/")
    def index():
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

        return render_template("index.html",
                               notes=notes,
                               current_filter=task_filter,
                               search_query=search_query)

    # Calendar route
    @app.route("/calendar")
    def calendar_view():
        return render_template("calendar.html")

    # Route to add a new note
    @app.route("/add-note", methods=["POST"])
    def add_note():
        content = request.form.get("content")
        task_id = request.form.get("task_id", 1, type=int)

        if content:
            note_manager.create_note(task_id=task_id, content=content)

        return redirect(url_for("index"))

    # Route to edit a note
    @app.route("/edit-note/<int:note_id>", methods=["POST"])
    def edit_note(note_id):
        new_content = request.form.get("content")

        if new_content:
            note_manager.update_note(note_id, new_content)

        return redirect(url_for("index"))

    # Route to delete a note
    @app.route("/delete-note/<int:note_id>")
    def delete_note(note_id):
        note_manager.delete_note(note_id)
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)