from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserProfile:
    profile_id: Optional[int]
    user_id: int
    bio: str
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        now = datetime.utcnow()
        if self.created_at is None:
            self.created_at = now
        if self.updated_at is None:
            self.updated_at = now