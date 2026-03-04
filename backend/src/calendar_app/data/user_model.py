from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class User:
    id: str
    email: str
    password_hash: str
    role: str  # "user" or "admin"
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(email: str, password_hash: str, role: str = "user"):
        now = datetime.utcnow()
        return User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=password_hash,
            role=role,
            created_at=now,
            updated_at=now
        )