from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from enum import Enum

class Semester(str, Enum):
    FALL = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"

class Enrollment(BaseModel):
    course_id: int = Field(..., gt=0)
    course_name: str = Field(..., min_length=3, max_length=100)
    semester: Semester
    grade: Optional[float] = Field(None, ge=0.0, le=4.0)

class Student(BaseModel):
    student_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=18, le=100)
    email: EmailStr
    enrollments: List[Enrollment] = []
