from fastapi import APIRouter, HTTPException, Request, status, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db
import models
import crud
import schemas
from typing import List
import asyncio

# Note: We are using schemas from models.py as per our earlier update
# but for clarity let's assume we use schemas.py or just use the ones in models.py
# I previously put schemas in models.py, so I will import from there.

import models as schemas 

enrollment_router = APIRouter()

# Setup Jinja2 template engine
templates = Jinja2Templates(directory="templates")
templates.env.globals.update(hasattr=hasattr)

# Helper for seeding courses
def seed_courses(db: Session):
    courses = [
        "FastAPI Development",
        "Python for Data Science",
        "Web Design with Jinja2",
        "Advanced API Security"
    ]
    for course_name in courses:
        if not db.query(models.Course).filter(models.Course.name == course_name).first():
            db.add(models.Course(name=course_name))
    db.commit()

# --- API Endpoints ---

@enrollment_router.get("/students/", response_model=List[schemas.StudentSchema])
async def get_students(db: Session = Depends(get_db)):
    """Return all students."""
    # await asyncio.sleep(1) # Simulated delay
    return crud.get_students(db)

@enrollment_router.get("/students/{student_id}", response_model=schemas.StudentSchema)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    """Return a single student by ID."""
    student = crud.get_student(db, student_id)
    if student:
        return student
    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} was not found"
    )

@enrollment_router.post("/students/", response_model=schemas.StudentSchema, status_code=status.HTTP_201_CREATED)
async def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Add a new student."""
    db_student = crud.get_student(db, student.student_id)
    if db_student:
        raise HTTPException(
            status_code=400,
            detail=f"Student with ID {student.student_id} already exists"
        )
    return crud.create_student(db, student)

@enrollment_router.put("/students/{student_id}", response_model=schemas.StudentSchema)
async def update_student(student_id: int, updated_student: schemas.StudentCreate, db: Session = Depends(get_db)):
    """Update an existing student."""
    db_student = crud.update_student(db, student_id, updated_student)
    if db_student:
        return db_student
    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} was not found"
    )

@enrollment_router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Remove a student."""
    if crud.delete_student(db, student_id):
        return
    raise HTTPException(
        status_code=404,
        detail=f"Student with ID {student_id} was not found"
    )

@enrollment_router.get("/courses/", response_model=List[schemas.CourseSchema])
async def get_courses(db: Session = Depends(get_db)):
    """Return all available courses."""
    seed_courses(db)
    return crud.get_courses(db)

@enrollment_router.get("/courses-sync/")
def get_courses_sync(db: Session = Depends(get_db)):
    """Sync version for internal use or simple testing."""
    seed_courses(db)
    return crud.get_courses(db)

# --- HTML Routes ---

@enrollment_router.get("/home", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    seed_courses(db)
    students = crud.get_students(db)
    courses = crud.get_courses(db)
    return templates.TemplateResponse("enrollment.html", {
        "request": request,
        "enrollments": students,
        "enrollment": None,
        "available_courses": courses
    })

@enrollment_router.post("/home", response_class=HTMLResponse)
async def create_student_form(request: Request, item: str = Form(...), db: Session = Depends(get_db)):
    # Simple ID generation for the student_id (ui requirement)
    # In a real app, this might be handled differently
    last_student = db.query(models.Student).order_by(models.Student.student_id.desc()).first()
    new_student_id = (last_student.student_id + 1) if last_student else 1
    
    new_student = schemas.StudentCreate(
        student_id=new_student_id,
        name=item,
        age=20,
        email=f"{item.lower().replace(' ', '.')}@example.com"
    )
    crud.create_student(db, new_student)
    
    students = crud.get_students(db)
    courses = crud.get_courses(db)
    return templates.TemplateResponse("enrollment.html", {
        "request": request,
        "enrollments": students,
        "enrollment": None,
        "available_courses": courses
    })

@enrollment_router.get("/enrollment/{id}", response_class=HTMLResponse)
async def get_item_page(request: Request, id: int, db: Session = Depends(get_db)):
    # Note: id here is the student_id from the UI
    student = crud.get_student(db, id)
    if student:
        courses = crud.get_courses(db)
        return templates.TemplateResponse("enrollment.html", {
            "request": request,
            "enrollment": student,
            "enrollments": [],
            "available_courses": courses
        })
    raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")

@enrollment_router.post("/enrollment/{id}", response_class=HTMLResponse)
async def add_enrollment_form(request: Request, id: int, course_id: int = Form(...), semester: str = Form(...), db: Session = Depends(get_db)):
    student = crud.get_student(db, id)
    if student:
        new_enrollment = schemas.EnrollmentCreate(
            course_id=course_id,
            semester=semester,
            grade=None
        )
        crud.create_student_enrollment(db, student.id, new_enrollment)
        
        courses = crud.get_courses(db)
        return templates.TemplateResponse("enrollment.html", {
            "request": request,
            "enrollment": student,
            "enrollments": [],
            "available_courses": courses
        })
    raise HTTPException(status_code=404, detail=f"Student with ID {id} not found")
