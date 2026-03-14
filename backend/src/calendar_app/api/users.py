from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/users", tags=["users"])

class User(BaseModel):
    username: str
    email: str

USERS = [
    User(username="admin", email="admin@test.com"),
    User(username="user", email="user@test.com"),
]

@router.get("/users", response_model=List[User])
def list_users():
    return USERS

@router.get("/{username}", response_model=User)
def get_user(username: str):
    for user in USERS:
        if user.username == username:
            return user
        else:
            return None
    return None
