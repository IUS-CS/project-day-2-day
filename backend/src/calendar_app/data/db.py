# calendar_app/data/db.py
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
def init_db(url="sqlite:///calendar.db"):
    engine = create_engine(url, echo=False)

    with engine.connect() as conn:

        # Create notes table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS notes (
                note_id INTEGER PRIMARY KEY,
                task_id INTEGER NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'General',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """))
        # Backfill older databases that predate note categories.
        notes_columns = [row[1] for row in conn.execute(text("PRAGMA table_info(notes)"))]
        if "category" not in notes_columns:
            conn.execute(text("ALTER TABLE notes ADD COLUMN category TEXT NOT NULL DEFAULT 'General'"))

        # Create users table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """))

        # Create profiles table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS profiles (
                profile_id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                bio TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
        """))

        # Create completion table
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS task_completions (
    id INTEGER PRIMARY KEY,
    task_id INTEGER NOT NULL UNIQUE,
    completed BOOLEAN NOT NULL DEFAULT 0,
    completed_at DATETIME
             );
        """ ))

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS custom_notifications (
                id INTEGER PRIMARY KEY,
                message TEXT NOT NULL,
                level TEXT NOT NULL DEFAULT 'info',
                due_date TEXT,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL
            );
        """))
        custom_notification_columns = [
            row[1] for row in conn.execute(text("PRAGMA table_info(custom_notifications)"))
        ]
        if "due_date" not in custom_notification_columns:
            conn.execute(text("ALTER TABLE custom_notifications ADD COLUMN due_date TEXT"))
        conn.commit()

    return sessionmaker(bind=engine, expire_on_commit=False)