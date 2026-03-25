# calendar_app/data/note_model.py
# This file defines the Note data model and its corresponding SQLAlchemy ORM model.
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class Note:
    id: int
    task_id: int
    content: str
    created_at: datetime

    @staticmethod
    def create(task_id: int, content: str):
        return Note(
            id=uuid.uuid4().int >> 64,  # convert UUID to int
            task_id=task_id,
            content=content,
            created_at=datetime.utcnow()
        )


# --- SQLAlchemy ORM model ---
from sqlalchemy import Column, Integer, String, DateTime
from calendar_app.data.db import Base

class NoteORM(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)