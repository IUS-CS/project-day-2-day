from calendar_app.models.Note import Note


class NoteManager:
    """Handles creation, updating, deletion, and retrieval of notes."""

    def __init__(self, note_repo):
        self.note_repo = note_repo

    def create_note(self, task_id: int, content: str) -> Note:
        """Create a new note and save it."""
        next_id = self.note_repo.get_next_id()  # Always fetch fresh ID
        note = Note(task_id=task_id, content=content, note_id=next_id)
        return self.note_repo.save(note)

    def update_note(self, note_id: int, new_content: str) -> Note:
        note = self.note_repo.get(note_id)
        if not note:
            raise ValueError("Note not found")

        note.update_content(new_content)
        return self.note_repo.save(note)

    def delete_note(self, note_id: int) -> None:
        self.note_repo.delete(note_id)

    def get_note(self, note_id: int) -> Note:
        return self.note_repo.get(note_id)

    def get_all_notes(self):
        return self.note_repo.get_all()

    def get_notes_for_task(self, task_id: int):
        notes = self.note_repo.get_all()
        return [n for n in notes if n.task_id == task_id]

    def search_notes(self, query: str):
        query = query.lower()
        notes = self.note_repo.get_all()
        return [n for n in notes if query in n.content.lower()]