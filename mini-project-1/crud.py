from sqlalchemy.orm import Session
import models

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.student_id == student_id).first()

def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Student).offset(skip).limit(limit).all()

def create_student(db: Session, student: models.StudentCreate):
    db_student = models.Student(
        student_id=student.student_id,
        name=student.name,
        age=student.age,
        email=student.email
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student: models.StudentCreate):
    db_student = get_student(db, student_id)
    if db_student:
        db_student.name = student.name
        db_student.age = student.age
        db_student.email = student.email
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

def get_courses(db: Session):
    return db.query(models.Course).all()

def get_course(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def create_course(db: Session, name: str):
    db_course = models.Course(name=name)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

def create_student_enrollment(db: Session, student_id: int, enrollment: models.EnrollmentCreate):
    # student_id here is the SQLAlchemy primary key 'id'
    db_enrollment = models.Enrollment(
        student_id=student_id,
        course_id=enrollment.course_id,
        semester=enrollment.semester,
        grade=enrollment.grade
    )
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment
