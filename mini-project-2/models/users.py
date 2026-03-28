from beanie import Document
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class User(Document):
    email: EmailStr
    password: str
    events: Optional[List[str]] = []

    class Settings:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongPassword123"
            }
        }

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongPassword123"
            }
        }
