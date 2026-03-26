from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base

# --- SQLAlchemy Models ---

class Semester(str, Enum):
    FALL = "Fall"
    SPRING = "Spring"
    SUMMER = "Summer"

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    enrollments = relationship("Enrollment", back_populates="course")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, unique=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)

    enrollments = relationship("Enrollment", back_populates="student")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    semester = Column(SQLEnum(Semester))
    grade = Column(Float, nullable=True)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

    @property
    def course_name(self):
        return self.course.name if self.course else "Unknown Course"

# --- Pydantic Schemas ---

class EnrollmentBase(BaseModel):
    course_id: int = Field(..., gt=0)
    semester: Semester
    grade: Optional[float] = Field(None, ge=0.0, le=4.0)

class EnrollmentCreate(EnrollmentBase):
    pass

class EnrollmentSchema(EnrollmentBase):
    id: int
    course_name: str

    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    student_id: int = Field(..., gt=0)
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=18, le=100)
    email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentSchema(StudentBase):
    id: int
    enrollments: List[EnrollmentSchema] = []

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    name: str

class CourseSchema(CourseBase):
    id: int

    class Config:
        from_attributes = True
