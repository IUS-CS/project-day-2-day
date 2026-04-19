from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/assignments", tags=["assignments"])

class Assignment(BaseModel):
    name: str
    description: str

ASSIGNMENTS = [
    Assignment(name="Assignment 1", description="Show all work")
]

@router.get("", response_model=List[Assignment])
def list_assignments():
    return ASSIGNMENTS

@router.post("", response_model=Assignment)
def create_assignment(assignment: Assignment):
    ASSIGNMENTS.append(assignment)
    return assignment