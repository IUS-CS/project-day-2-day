from sqlalchemy import text
from calendar_app.data.user_model import User


class UserRepo:
    def __init__(self, SessionFactory):
        self.SessionFactory = SessionFactory

    def get_next_id(self):
        session = self.SessionFactory()
        result = session.execute(text("SELECT MAX(user_id) FROM users")).scalar()
        session.close()
        return (result or 0) + 1

    def save(self, user: User) -> User:
        session = self.SessionFactory()

        session.execute(
            text("""
                INSERT OR REPLACE INTO users
                (user_id, username, email, created_at, updated_at)
                VALUES (:user_id, :username, :email, :created_at, :updated_at)
            """),
            {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat(),
            }
        )

        session.commit()
        session.close()
        return user

    def get(self, user_id: int) -> User | None:
        session = self.SessionFactory()
        row = session.execute(
            text("SELECT * FROM users WHERE user_id = :id"),
            {"id": user_id}
        ).fetchone()
        session.close()

        if not row:
            return None

        return User(
            user_id=row["user_id"],
            username=row["username"],
            email=row["email"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def get_all(self):
        session = self.SessionFactory()
        rows = session.execute(text("SELECT * FROM users")).fetchall()
        session.close()

        return [
            User(
                user_id=row["user_id"],
                username=row["username"],
                email=row["email"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            for row in rows
        ]