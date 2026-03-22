from fastapi import FastAPI
from enrollment import enrollment_router

app = FastAPI(title="Course Enrollment API")

@app.get("/")
async def welcome() -> dict:
    return {"message": "Welcome to the Course Enrollment API"}

app.include_router(enrollment_router)
