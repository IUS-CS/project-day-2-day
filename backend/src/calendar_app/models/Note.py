from datetime import datetime
from typing import Optional
from backend.src.calendar_app.utils.validators import validate_note_content


class Note:
    """
    Represents a note attached to a task.

    Attributes:
        id: Unique identifier for the note
        task_id: ID of the task this note belongs to
        content: The text content of the note

    """

    def __init__(self, task_id: int, content: str, note_id: Optional[int] = None):
        """
        Initialize a new Note.

        Args:
            task_id: ID of the task this note belongs to
            content: Text content of the note
            note_id: Optional existing note ID (for loading from database)
        """
        if not validate_note_content(content):
            raise ValueError("Invalid note content")

        self.id = note_id
        self.task_id = task_id
        self.content = content.strip()
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_content(self, new_content: str) -> None:
        if not validate_note_content(new_content):
            raise ValueError("Invalid note content")

        self.content = new_content.strip()
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert note to dictionary representation."""
        return {
            'id': self.id,
            'task_id': self.task_id,
            'content': self.content,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Note':
        """Create a Note instance from a dictionary."""
        note = cls(
            task_id=data['task_id'],
            content=data['content'],
            note_id=data.get('id')
        )

        if 'created_at' in data:
            note.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            note.updated_at = datetime.fromisoformat(data['updated_at'])

        return note