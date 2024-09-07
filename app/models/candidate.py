# Importing necessary libraries
from pydantic import BaseModel, EmailStr  # Pydantic BaseModel for data validation, EmailStr for email validation
from typing import List, Literal  # List for typing lists of values, Literal for defining allowed values
from uuid import uuid4  # UUID generation for unique identification
from typing import Optional  # Optional to allow some fields to be optional

# Define the Candidate class that extends from Pydantic's BaseModel for validation and data handling
class Candidate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    uuid: str = str(uuid4())
    career_level: str
    job_major: str
    years_of_experience: int
    degree_type: str
    skills: List[str]
    nationality: str
    city: str
    salary: float
    gender: Literal['Male', 'Female', 'NotSpecified']
    user_id: Optional[str] = None
