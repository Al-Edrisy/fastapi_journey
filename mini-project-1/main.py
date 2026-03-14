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

@app.post("/students/", response_model=Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: Student):
    """Add a new student."""
    # Check if student_id already exists
    for s in students_db:
        if s.student_id == student.student_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Student with ID {student.student_id} already exists"
            )
    students_db.append(student)
    return student

@app.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: int, updated_student: Student):
    """Update an existing student."""
    for idx, student in enumerate(students_db):
        if student.student_id == student_id:
            students_db[idx] = updated_student
            return updated_student
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with ID {student_id} not found"
    )

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: int):
    """Remove a student."""
    for idx, student in enumerate(students_db):
        if student.student_id == student_id:
            students_db.pop(idx)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Student with ID {student_id} not found"
    )
