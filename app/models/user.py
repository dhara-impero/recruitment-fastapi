# Importing necessary libraries
from pydantic import BaseModel, EmailStr  # BaseModel for validation and EmailStr for validating email addresses
from uuid import uuid4  # UUID generation for creating unique identifiers
from typing import Optional  # Optional for fields that can be optionally included


# Define the User class that extends Pydantic's BaseModel
class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    UUID: str = str(uuid4())

# Define the UserResponseModel class, used to represent user data in API responses
class UserResponseModel(BaseModel):
    _id: str
    first_name: str
    last_name: str
    email: EmailStr
    UUID: str = str(uuid4())