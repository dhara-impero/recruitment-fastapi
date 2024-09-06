from fastapi import APIRouter, Depends, Query
from app.dtos.user_dto import User
from app.dtos.candidate_dto import Candidate
from app.controller.candidate_controller import CandidateController
from typing import Optional,List, Literal
from app.dtos.user_dto import UserResponseModel
from app.helper.token_helper import TokenHelper

candidate = APIRouter()

@candidate.post("/candidate")
def create_candidate(candidate: Candidate, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    return CandidateController.create_candidate(candidate, current_user)

@candidate.get("/candidate/{candidate_id}")
def get_candidate(candidate_id: str, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    return CandidateController.get_candidate(candidate_id, current_user)

@candidate.delete("/candidate/{candidate_id}")
def delete_candidate(candidate_id: str, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    return CandidateController.delete_candidate(candidate_id, current_user)

@candidate.put("/candidate/{candidate_id}")
def edit_candidate(candidate_id: str,updated_candidate: Candidate, current_user: UserResponseModel = Depends(TokenHelper.verify_token)):
    return CandidateController.edit_candidate(candidate_id,updated_candidate, current_user)

@candidate.get("/generate-report")
def generate_report():
    return CandidateController.generate_report()

@candidate.get("/all-candidates")
def get_all_candidates(
    current_user: UserResponseModel = Depends(TokenHelper.verify_token),
    first_name: Optional[str] = Query(None),
    last_name: Optional[str] = Query(None),
    email: Optional[str] = Query(None),
    career_level: Optional[str] = Query(None),
    job_major: Optional[str] = Query(None),
    years_of_experience: Optional[int] = Query(None),
    degree_type: Optional[str] = Query(None),
    skills: Optional[List[str]] = Query(None),
    nationality: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    salary_min: Optional[float] = Query(None),
    salary_max: Optional[float] = Query(None),
    gender: Optional[Literal['Male', 'Female', 'NotSpecified']] = Query(None),
    search: Optional[str] = Query(None)
):
    return CandidateController.get_all_candidates(
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