from fastapi import APIRouter, Depends
from app.dtos.user_dto import User
from app.dtos.candidate_dto import Candidate
from app.controller.candidate_controller import CandidateController

candidate = APIRouter()

@candidate.post("/candidate")
def create_candidate(candidate: Candidate):
    return CandidateController.create_candidate(candidate)

@candidate.get("/candidate/{candidate_id}")
def get_candidate(candidate_id: str):
    return CandidateController.get_candidate(candidate_id)

# Add more routes for update, delete, etc.