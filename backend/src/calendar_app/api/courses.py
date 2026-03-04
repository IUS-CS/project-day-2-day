from fastapi import APIRouter, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List

router = APIRouter(prefix="/courses", tags=["courses"])
templates = Jinja2Templates(directory="templates")

class Course(BaseModel):
    name: str
    course_id: int
    description: str

COURSES = [
    Course(name="Software Engineering", course_id=18904, description="Software Engineering")
]

@router.get("/", response_class=HTMLResponse)
def courses_page(request: Request):
    return templates.TemplateResponse("courses.html", {"request": request, "courses": COURSES})

@router.get("/courses", response_model=List[Course])
def list_courses():
    return COURSES

@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    for course in COURSES:
        if course.course_id == course_id:
            return course
    return None
