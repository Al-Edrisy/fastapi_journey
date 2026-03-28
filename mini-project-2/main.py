from fastapi import FastAPI
from database.connection import initialize_database
from routes.events import event_router
from routes.users import user_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    await initialize_database()

app.include_router(event_router, prefix="/event", tags=["Events"])
app.include_router(user_router, prefix="/user", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Event Planner API"}
