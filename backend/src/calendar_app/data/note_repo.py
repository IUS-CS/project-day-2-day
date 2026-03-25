from calendar_app.models.Note import Note
from datetime import datetime
from sqlalchemy import text


class NoteRepo:
    """Database-backed repository for notes."""

    def __init__(self, SessionFactory):
        self.SessionFactory = SessionFactory

    def get_next_id(self) -> int:
        session = self.SessionFactory()
        result = session.execute(text("SELECT MAX(note_id) FROM notes")).scalar()
        session.close()
        return (result or 0) + 1

    def save(self, note: Note) -> Note:
        session = self.SessionFactory()

        session.execute(
            text("""
                INSERT OR REPLACE INTO notes 
                (note_id, task_id, content, created_at, updated_at)
                VALUES (:note_id, :task_id, :content, :created_at, :updated_at)
            """),
            {
                "note_id": note.note_id,
                "task_id": note.task_id,
                "content": note.content,
                "created_at": note.created_at.isoformat(),
                "updated_at": note.updated_at.isoformat(),
            },
        )

        session.commit()
        session.close()
        return note

    def get(self, note_id: int) -> Note | None:
        session = self.SessionFactory()
        row = session.execute(
            text("SELECT * FROM notes WHERE note_id = :id"),
            {"id": note_id}
        ).mappings().fetchone()
        session.close()

        if not row:
            return None

        return Note(
            task_id=row["task_id"],
            content=row["content"],
            note_id=row["note_id"],
        )

    def delete(self, note_id: int) -> None:
        session = self.SessionFactory()
        session.execute(
            text("DELETE FROM notes WHERE note_id = :id"),
            {"id": note_id}
        )
        session.commit()
        session.close()

    def get_all(self):
        session = self.SessionFactory()
        rows = session.execute(
            text("SELECT * FROM notes")
        ).mappings().all()
        session.close()

        return [
            Note(
                task_id=row["task_id"],
                content=row["content"],
                note_id=row["note_id"],
            )
            for row in rows
        ]