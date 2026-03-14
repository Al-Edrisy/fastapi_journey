# Architectural Decisions - Mini Project 1

This document explains the design choices made for the Course Enrollment API.

## 1. Pydantic Field Types

I chose the following field types for the `Student` and `Enrollment` models:

- **`int` (student_id, course_id, age)**: Used for unique identifiers and age because these values are naturally whole numbers.
- **`str` (name, course_name, email)**: Used for textual data. I used `EmailStr` (inheriting from str) for the email field to ensure basic format validation.
- **`float` (grade)**: Used for grades because they can include decimals (e.g., 3.5).
- **`Enum` (semester)**: Used fixed values (`FALL`, `SPRING`, `SUMMER`) to prevent invalid semester entries like "Winter" or "Random".
- **`List[Enrollment]`**: Used to represent the one-to-many relationship where a student can have multiple enrollments.

## 2. Validation Rules

The models implement the following validation rules to maintain data integrity:

- **`gt=0` (student_id, course_id)**: Protects against invalid IDs (negative numbers or zero), ensuring every entity has a valid positive identifier.
- **`ge=18, le=100` (age)**: Ensures the student is within a realistic age range for enrollment (adults up to 100 years old).
- **`min_length=2` (name)**: Protects against empty or single-character names which are usually data entry errors.
- **`ge=0.0, le=4.0` (grade)**: Constraints the grade to a standard GPA scale, preventing impossible values like -5 or 10.
- **`Enum` (semester)**: Acts as a structural validation, rejecting any value not explicitly defined in the `Semester` enum.

## 3. Async Endpoints

All endpoints are defined using `async def` to leverage FastAPI's asynchronous capabilities. 

The **`GET /students/`** endpoint uses `await asyncio.sleep(1)` to meaningfully simulate a real-world scenario where the API would wait for a response from an external database or service. This demonstrates how the event loop can handle other requests while waiting for I/O-bound operations to complete, preventing the server from blocking.
