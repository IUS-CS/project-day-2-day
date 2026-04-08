from calendar_app.data.task_completion_model import TaskCompletion
from datetime import datetime
from sqlalchemy import text


class TaskCompletionRepo:
    """Database-backed repository for task completion status."""

    def __init__(self, SessionFactory):
        self.SessionFactory = SessionFactory

    def get_next_id(self) -> int:
        session = self.SessionFactory()
        result = session.execute(text("SELECT MAX(id) FROM task_completions")).scalar()
        session.close()
        return (result or 0) + 1

    def mark_complete(self, task_id: int) -> TaskCompletion:
        """Mark a task as complete."""
        session = self.SessionFactory()

        # Check if record exists
        existing = session.execute(
            text("SELECT * FROM task_completions WHERE task_id = :task_id"),
            {"task_id": task_id}
        ).mappings().fetchone()

        if existing:
            # Update existing record
            session.execute(
                text("""
                     UPDATE task_completions
                     SET completed    = 1,
                         completed_at = :completed_at
                     WHERE task_id = :task_id
                     """),
                {
                    "task_id": task_id,
                    "completed_at": datetime.utcnow().isoformat()
                }
            )
        else:
            # Insert new record
            session.execute(
                text("""
                     INSERT INTO task_completions (id, task_id, completed, completed_at)
                     VALUES (:id, :task_id, :completed, :completed_at)
                     """),
                {
                    "id": self.get_next_id(),
                    "task_id": task_id,
                    "completed": True,
                    "completed_at": datetime.utcnow().isoformat()
                }
            )

        session.commit()
        session.close()

        return self.get(task_id)

    def mark_incomplete(self, task_id: int) -> TaskCompletion:
        """Mark a task as incomplete."""
        session = self.SessionFactory()

        # Check if record exists
        existing = session.execute(
            text("SELECT * FROM task_completions WHERE task_id = :task_id"),
            {"task_id": task_id}
        ).mappings().fetchone()

        if existing:
            # Update existing record
            session.execute(
                text("""
                     UPDATE task_completions
                     SET completed    = 0,
                         completed_at = NULL
                     WHERE task_id = :task_id
                     """),
                {"task_id": task_id}
            )
        else:
            # Insert new record
            session.execute(
                text("""
                     INSERT INTO task_completions (id, task_id, completed, completed_at)
                     VALUES (:id, :task_id, :completed, :completed_at)
                     """),
                {
                    "id": self.get_next_id(),
                    "task_id": task_id,
                    "completed": False,
                    "completed_at": None
                }
            )

        session.commit()
        session.close()

        return self.get(task_id)

    def toggle(self, task_id: int) -> bool:
        """Toggle a task's completion status. Returns new status."""
        if self.is_complete(task_id):
            self.mark_incomplete(task_id)
            return False
        else:
            self.mark_complete(task_id)
            return True

    def get(self, task_id: int) -> TaskCompletion | None:
        """Get completion status for a task."""
        session = self.SessionFactory()
        row = session.execute(
            text("SELECT * FROM task_completions WHERE task_id = :task_id"),
            {"task_id": task_id}
        ).mappings().fetchone()
        session.close()

        if not row:
            return None

        return TaskCompletion(
            id=row["id"],
            task_id=row["task_id"],
            completed=bool(row["completed"]),
            completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None
        )

    def is_complete(self, task_id: int) -> bool:
        """Check if a task is marked complete."""
        completion = self.get(task_id)
        return completion.completed if completion else False

    def get_all_completed(self):
        """Get all completed tasks."""
        session = self.SessionFactory()
        rows = session.execute(
            text("SELECT * FROM task_completions WHERE completed = 1")
        ).mappings().all()
        session.close()

        return [
            TaskCompletion(
                id=row["id"],
                task_id=row["task_id"],
                completed=bool(row["completed"]),
                completed_at=datetime.fromisoformat(row["completed_at"]) if row["completed_at"] else None
            )
            for row in rows
        ]

    def get_stats(self, all_task_ids: list[int]) -> dict:
        """Get completion statistics for a list of tasks."""
        session = self.SessionFactory()

        # Count completed tasks
        completed_count = 0
        for task_id in all_task_ids:
            if self.is_complete(task_id):
                completed_count += 1

        session.close()

        total = len(all_task_ids)
        incomplete = total - completed_count
        completion_rate = (completed_count / total * 100) if total > 0 else 0

        return {
            'total': total,
            'completed': completed_count,
            'incomplete': incomplete,
            'completion_rate': round(completion_rate, 1)
        }

    def add_completion_status_to_tasks(self, tasks: list[dict]) -> list[dict]:
        """Add completion status to a list of task dictionaries."""
        result = []
        for task in tasks:
            task_copy = task.copy()
            completion = self.get(task['id'])
            task_copy['completed'] = completion.completed if completion else False
            task_copy['completed_at'] = completion.completed_at if completion else None
            result.append(task_copy)
        return result