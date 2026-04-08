# calendar_app/data/task_completion_model.py
# This file defines the TaskCompletion data model and its corresponding SQLAlchemy ORM model.
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class TaskCompletion:
    id: int
    task_id: int
    completed: bool
    completed_at: datetime

    @staticmethod
    def create(task_id: int, completed: bool = False):
        return TaskCompletion(
            id=uuid.uuid4().int >> 64,  # convert UUID to int
            task_id=task_id,
            completed=completed,
            completed_at=datetime.utcnow() if completed else None
        )


# --- SQLAlchemy ORM model ---
from sqlalchemy import Column, Integer, Boolean, DateTime
from calendar_app.data.db import Base

class TaskCompletionORM(Base):
    __tablename__ = "task_completions"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False, unique=True)  # One completion record per task
    completed = Column(Boolean, nullable=False, default=False)
    completed_at = Column(DateTime, nullable=True)