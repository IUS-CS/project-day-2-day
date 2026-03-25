from sqlalchemy import text
from calendar_app.data.profile_model import UserProfile


class ProfileRepo:
    def __init__(self, SessionFactory):
        self.SessionFactory = SessionFactory

    def get_next_id(self):
        session = self.SessionFactory()
        result = session.execute(text("SELECT MAX(profile_id) FROM profiles")).scalar()
        session.close()
        return (result or 0) + 1

    def save(self, profile: UserProfile) -> UserProfile:
        session = self.SessionFactory()

        session.execute(
            text("""
                INSERT OR REPLACE INTO profiles
                (profile_id, user_id, bio, created_at, updated_at)
                VALUES (:profile_id, :user_id, :bio, :created_at, :updated_at)
            """),
            {
                "profile_id": profile.profile_id,
                "user_id": profile.user_id,
                "bio": profile.bio,
                "created_at": profile.created_at.isoformat(),
                "updated_at": profile.updated_at.isoformat(),
            }
        )

        session.commit()
        session.close()
        return profile

    def get(self, profile_id: int) -> UserProfile | None:
        session = self.SessionFactory()
        row = session.execute(
            text("SELECT * FROM profiles WHERE profile_id = :id"),
            {"id": profile_id}
        ).fetchone()
        session.close()

        if not row:
            return None

        return UserProfile(
            profile_id=row["profile_id"],
            user_id=row["user_id"],
            bio=row["bio"],
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

    def get_all(self):
        session = self.SessionFactory()
        rows = session.execute(text("SELECT * FROM profiles")).fetchall()
        session.close()

        return [
            UserProfile(
                profile_id=row["profile_id"],
                user_id=row["user_id"],
                bio=row["bio"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            for row in rows
        ]