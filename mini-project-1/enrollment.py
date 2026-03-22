from fastapi import APIRouter, HTTPException, Request, status, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Student, Enrollment
from typing import List
import asyncio

enrollment_router = APIRouter()

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(hasattr=hasattr)

# Mock database (moved from main.py)
students_db: List[Student] = []

# Mock courses database
courses_db = [
    {"id": 101, "name": "FastAPI Development"},
    {"id": 102, "name": "Python for Data Science"},
    {"id": 103, "name": "Web Design with Jinja2"},
    {"id": 104, "name": "Advanced API Security"}
]

# --- API Endpoints ---

@enrollment_router.get("/students/", response_model=List[Student])
async def get_students():
    """Return all students."""
    await asyncio.sleep(1)
    return students_db

@enrollment_router.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: int):
    """Return a single student by ID."""
    for student in students_db:
        if student.student_id == student_id:
            return student
    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} was not found"
    )

@enrollment_router.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):
    """Add a new student."""
    for s in students_db:
        if s.student_id == student.student_id:
            raise HTTPException(
                status_code=400,
                detail=f"Student with ID {student.student_id} already exists"
            )
    students_db.append(student)
    return student

@enrollment_router.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, updated_student: Student):
    """Update an existing student."""
    for idx, student in enumerate(students_db):
        if student.student_id == student_id:
            students_db[idx] = updated_student
            return updated_student
    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} was not found"
    )

@enrollment_router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int):
    """Remove a student."""
    for idx, student in enumerate(students_db):
        if student.student_id == student_id:
            students_db.pop(idx)
            return
    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} was not found"
    )

@enrollment_router.get("/courses/")
async def get_courses():
    """Return all available courses."""
    return courses_db

# --- HTML Routes ---

@enrollment_router.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("enrollment.html", {
        "request": request,
        "enrollments": students_db,
        "enrollment": None,
        "available_courses": courses_db
    })

@enrollment_router.post("/home", response_class=HTMLResponse)
async def create_student_form(request: Request, item: str = Form(...)):
    # Generate a simple ID
    new_id = len(students_db) + 1
    # Create student with some defaults since form is limited
    new_student = Student(
        student_id=new_id,
        name=item,
        age=20,
        email=f"{item.lower().replace(' ', '.')}@example.com"
    )
    students_db.append(new_student)
    return templates.TemplateResponse("enrollment.html", {
        "request": request,
        "enrollments": students_db,
        "enrollment": None,
        "available_courses": courses_db
    })

@enrollment_router.get("/enrollment/{id}", response_class=HTMLResponse)
async def get_item_page(request: Request, id: int):
    for student in students_db:
        if student.student_id == id:
            # Map student to what enrollment.html expects if needed, 
            # or we will adapt the template to use the student object.
            return templates.TemplateResponse("enrollment.html", {
                "request": request,
                "enrollment": student,
                "enrollments": [],
                "available_courses": courses_db
            })
    raise HTTPException(status_code=404, detail=f"Enrollment with ID {id} not found")

@enrollment_router.post("/enrollment/{id}", response_class=HTMLResponse)
async def add_enrollment_form(request: Request, id: int, course_id: int = Form(...), semester: str = Form(...)):
    for student in students_db:
        if student.student_id == id:
            # Find course name from ID
            course_name = next((c["name"] for c in courses_db if c["id"] == course_id), "Unknown Course")
            
            new_enrollment = Enrollment(
                course_id=course_id,
                course_name=course_name,
                semester=semester,
                grade=None
            )
            student.enrollments.append(new_enrollment)
            return templates.TemplateResponse("enrollment.html", {
                "request": request,
                "enrollment": student,
                "enrollments": [],
                "available_courses": courses_db
            })
    raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
