from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    userid: str
    username: str
    password: str

class UserResponse(UserCreate):
    class Config:
        from_attributes = True
