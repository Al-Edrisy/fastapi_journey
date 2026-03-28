from beanie import Document
from pydantic import BaseModel
from typing import List, Optional

class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Settings:
        name = "events"

    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastAPI Mini Project 2 Lunch",
                "image": "https://example.com/image.png",
                "description": "A networking lunch for backend developers.",
                "tags": ["fastapi", "mongodb", "beanie"],
                "location": "Online"
            }
        }

class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Event Title",
                "location": "New York City"
            }
        }
