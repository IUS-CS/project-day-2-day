from dataclasses import dataclass
from typing import Optional

@dataclass
class UserProfile:
    user_id: str
    display_name: Optional[str] = None
    timezone: Optional[str] = "UTC"
    theme: Optional[str] = "light"
    notifications_enabled: bool = True