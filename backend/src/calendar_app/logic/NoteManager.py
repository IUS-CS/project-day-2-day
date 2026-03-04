from typing import List, Optional
from datetime import datetime
from backend.src.calendar_app.models.Note import Note


class NoteManager:

    def __init__(self):
        """Initialize the NoteManager."""
        # Temporary in-memory storage (replace with database later)
        self._notes = {}
        self._next_id = 1

    def create_note(self, task_id: int, content: str) -> Note:
        """
        Create a new note for a task.

        Args:
            task_id: ID of the task to attach the note to
            content: Text content of the note

        Returns:
            The created Note object

        """
        note = Note(task_id=task_id, content=content, note_id=self._next_id)
        self._notes[self._next_id] = note
        self._next_id += 1
        return note

    def get_note(self, note_id: int) -> Optional[Note]:
        """
        Retrieve a note by its ID.

        Args:
            note_id: ID of the note to retrieve

        Returns:
            The Note object if found, None otherwise
        """
        return self._notes.get(note_id)

    def get_notes_for_task(self, task_id: int) -> List[Note]:
        """
        Get all notes for a specific task.

        Args:
            task_id: ID of the task

        Returns:
            List of Note objects for the task
        """
        return [note for note in self._notes.values() if note.task_id == task_id]

    def get_all_notes(self) -> List[Note]:
        """
        Get all notes in the system.

        Returns:
            List of all Note objects
        """
        return list(self._notes.values())

    def update_note(self, note_id: int, new_content: str) -> Optional[Note]:
        """
        Update the content of an existing note.

        Args:
            note_id: ID of the note to update
            new_content: New text content for the note

        Returns:
            The updated Note object if found, None otherwise

        """
        note = self._notes.get(note_id)
        if note:
            note.update_content(new_content)
        return note

    def delete_note(self, note_id: int) -> bool:
        """
        Delete a note by its ID.

        Args:
            note_id: ID of the note to delete

        Returns:
            True if note was deleted, False if note was not found
        """
        if note_id in self._notes:
            del self._notes[note_id]
            return True
        return False

    def delete_notes_for_task(self, task_id: int) -> int:
        """
        Delete all notes for a specific task.

        Args:
            task_id: ID of the task

        Returns:
            Number of notes deleted
        """
        notes_to_delete = [note_id for note_id, note in self._notes.items()
                           if note.task_id == task_id]

        for note_id in notes_to_delete:
            del self._notes[note_id]

        return len(notes_to_delete)

    def count_notes_for_task(self, task_id: int) -> int:
        """
        Count how many notes a task has.

        Args:
            task_id: ID of the task

        Returns:
            Number of notes for the task
        """
        return len(self.get_notes_for_task(task_id))

    def search_notes(self, search_term: str) -> List[Note]:
        """
        Search notes by content.

        Args:
            search_term: Text to search for in note content

        Returns:
            List of Note objects containing the search term
        """
        if not search_term:
            return []

        search_term_lower = search_term.lower()
        return [note for note in self._notes.values()
                if search_term_lower in note.content.lower()]

    def get_recent_notes(self, limit: int = 10) -> List[Note]:
        """
        Get the most recently created notes.

        Args:
            limit: Maximum number of notes to return

        Returns:
            List of Note objects, sorted by creation time (newest first)
        """
        sorted_notes = sorted(self._notes.values(),
                              key=lambda n: n.created_at,
                              reverse=True)
        return sorted_notes[:limit]

    def get_recently_updated_notes(self, limit: int = 10) -> List[Note]:
        """
        Get the most recently updated notes.

        Args:
            limit: Maximum number of notes to return

        Returns:
            List of Note objects, sorted by update time (newest first)
        """
        sorted_notes = sorted(self._notes.values(),
                              key=lambda n: n.updated_at,
                              reverse=True)
        return sorted_notes[:limit]