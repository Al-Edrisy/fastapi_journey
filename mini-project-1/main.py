from fastapi import FastAPI
from enrollment import enrollment_router
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Course Enrollment API")

@app.get("/home")
async def welcome() -> dict:
    return {"message": "Welcome to the Course Enrollment API"}

app.include_router(enrollment_router)
