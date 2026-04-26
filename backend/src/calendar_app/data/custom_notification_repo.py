from datetime import datetime
from sqlalchemy import text


class CustomNotificationRepo:
    """Database-backed repository for user-created dashboard notifications."""

    def __init__(self, SessionFactory):
        self.SessionFactory = SessionFactory

    def get_next_id(self) -> int:
        session = self.SessionFactory()
        result = session.execute(text("SELECT MAX(id) FROM custom_notifications")).scalar()
        session.close()
        return (result or 0) + 1

    def create(self, message: str, level: str = "info", due_date: str | None = None) -> None:
        session = self.SessionFactory()
        session.execute(
            text("""
                INSERT INTO custom_notifications (id, message, level, due_date, is_active, created_at)
                VALUES (:id, :message, :level, :due_date, 1, :created_at)
            """),
            {
                "id": self.get_next_id(),
                "message": message.strip(),
                "level": level,
                "due_date": due_date,
                "created_at": datetime.utcnow().isoformat(),
            },
        )
        session.commit()
        session.close()

    def dismiss(self, notification_id: int) -> None:
        session = self.SessionFactory()
        session.execute(
            text("UPDATE custom_notifications SET is_active = 0 WHERE id = :id"),
            {"id": notification_id},
        )
        session.commit()
        session.close()

    def get_active(self):
        session = self.SessionFactory()
        rows = session.execute(
            text("""
                SELECT id, message, level, due_date, created_at
                FROM custom_notifications
                WHERE is_active = 1
                ORDER BY
                    CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END,
                    due_date ASC,
                    created_at DESC
            """)
        ).mappings().all()
        session.close()
        return [dict(row) for row in rows]
