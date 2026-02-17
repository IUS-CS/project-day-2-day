# This file defines a simple API endpoint to check if the backend is running.

from fastapi import APIRouter

router = APIRouter()

@router.get("/hello")
def hello():
    return {"message": "Backend is running"}