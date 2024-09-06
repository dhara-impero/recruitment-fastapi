from pydantic import BaseModel, EmailStr
from uuid import uuid4
from typing import Optional

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    UUID: str = str(uuid4())
    
class UserResponseModel(BaseModel):
    _id: str
    first_name: str
    last_name: str
    email: EmailStr
    UUID: str = str(uuid4())