# Import necessary libraries and modules
from fastapi import APIRouter, Depends, Query  # FastAPI components for creating routes, dependency injection, and query parameters
from app.models.user import User  # Import User model (though not used in the provided code)
from app.models.candidate import Candidate  # Import Candidate model for request body validation
from app.service.candidate_service import CandidateService  # Service class for candidate-related operations
from typing import Optional, List, Literal  # Type hints for optional, list, and literal types
from app.models.user import UserResponseModel  # Import UserResponseModel for response typing and authentication
from app.helper.token_helper import TokenHelper  # Import TokenHelper for token verification

# Create an APIRouter instance for routing candidate-related endpoints
candidate = APIRouter()

# Route to create a new candidate
@candidate.post("/candidate")
def create_candidate(candidate: Candidate, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    """
    Create a new candidate entry.
    
    - **candidate**: Candidate data for creation (validated with Candidate model)
    - **current_user**: The currently authenticated user (validated with TokenHelper)
    """
    return CandidateService.create_candidate(candidate, current_user)

# Route to retrieve a candidate by their ID
@candidate.get("/candidate/{candidate_id}")
def get_candidate(candidate_id: str, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    """
    Retrieve a candidate by their ID.
    
    - **candidate_id**: ID of the candidate to retrieve
    - **current_user**: The currently authenticated user (validated with TokenHelper)
    """
    return CandidateService.get_candidate(candidate_id, current_user)

# Route to delete a candidate by their ID
@candidate.delete("/candidate/{candidate_id}")
def delete_candidate(candidate_id: str, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    """
    Delete a candidate by their ID.
    
    - **candidate_id**: ID of the candidate to delete
    - **current_user**: The currently authenticated user (validated with TokenHelper)
    """
    return CandidateService.delete_candidate(candidate_id, current_user)

# Route to update (edit) a candidate's information
@candidate.put("/candidate/{candidate_id}")
def edit_candidate(candidate_id: str, updated_candidate: Candidate, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    """
    Update an existing candidate's information.
    
    - **candidate_id**: ID of the candidate to update
    - **updated_candidate**: New candidate data (validated with Candidate model)
    - **current_user**: The currently authenticated user (validated with TokenHelper)
    """
    return CandidateService.edit_candidate(candidate_id, updated_candidate, current_user)

# Route to generate a report (e.g., of all candidates or specific data)
@candidate.get("/generate-report")
def generate_report():
    """
    Generate a report based on candidate data.
    """
    return CandidateService.generate_report()

# Route to retrieve all candidates with optional filtering
@candidate.get("/all-candidates")
def get_all_candidates(
    current_user: UserResponseModel = Depends(TokenHelper.verify_token),
    first_name: Optional[str] = Query(None),  # Optional query parameter for filtering by first name
    last_name: Optional[str] = Query(None),  # Optional query parameter for filtering by last name
    email: Optional[str] = Query(None),  # Optional query parameter for filtering by email
    career_level: Optional[str] = Query(None),  # Optional query parameter for filtering by career level
    job_major: Optional[str] = Query(None),  # Optional query parameter for filtering by job major
    years_of_experience: Optional[int] = Query(None),  # Optional query parameter for filtering by years of experience
    degree_type: Optional[str] = Query(None),  # Optional query parameter for filtering by degree type
    skills: Optional[List[str]] = Query(None),  # Optional query parameter for filtering by skills (list of skills)
    nationality: Optional[str] = Query(None),  # Optional query parameter for filtering by nationality
    city: Optional[str] = Query(None),  # Optional query parameter for filtering by city
    salary_min: Optional[float] = Query(None),  # Optional query parameter for filtering by minimum salary
    salary_max: Optional[float] = Query(None),  # Optional query parameter for filtering by maximum salary
    gender: Optional[Literal['Male', 'Female', 'NotSpecified']] = Query(None),  # Optional query parameter for filtering by gender
    search: Optional[str] = Query(None)  # Optional query parameter for a free-text search
):
    """
    Retrieve a list of candidates with optional search.
    
    - **current_user**: The currently authenticated user (validated with TokenHelper)
    - **first_name**: Filter by candidate's first name
    - **last_name**: Filter by candidate's last name
    - **email**: Filter by candidate's email address
    - **career_level**: Filter by candidate's career level
    - **job_major**: Filter by candidate's job major
    - **years_of_experience**: Filter by candidate's years of experience
    - **degree_type**: Filter by candidate's degree type
    - **skills**: Filter by candidate's skills
    - **nationality**: Filter by candidate's nationality
    - **city**: Filter by candidate's city
    - **salary_min**: Filter by minimum salary
    - **salary_max**: Filter by maximum salary
    - **gender**: Filter by candidate's gender
    - **search**: Perform a free-text search across various fields
    """
    return CandidateService.get_all_candidates(
        current_user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        career_level=career_level,
        job_major=job_major,
        years_of_experience=years_of_experience,
        degree_type=degree_type,
        skills=skills,
        nationality=nationality,
        city=city,
        salary_min=salary_min,
        salary_max=salary_max,
        gender=gender,
        search=search
    )
