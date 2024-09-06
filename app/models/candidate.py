from pydantic import BaseModel, EmailStr
from typing import List, Literal
from uuid import uuid4
from typing import Optional

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
