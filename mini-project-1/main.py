import asyncio
from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Student, Enrollment

app = FastAPI(title="Course Enrollment API")

# In-memory storage for students
students_db = []

@app.get("/students/", response_model=List[Student])
async def get_students():
    """Return all students."""
    # Simulating a database fetch delay
    await asyncio.sleep(1)
    return students_db

@app.get("/students/{student_id}", response_model=Student)
async def get_student(student_id: int):
    """Return a single student by ID."""
    for student in students_db:
        if student.student_id == student_id:
            return student
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with ID {student_id} not found"
    )
