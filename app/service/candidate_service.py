# Import necessary libraries and modules
from app.repository.candidate_repository import CandidateRepository  # Import CandidateRepository for database operations
from app.models.candidate import Candidate  # Import Candidate model for type hinting and validation
from fastapi import HTTPException  # Import FastAPI components for handling HTTP exceptions
import logging  # Import logging for error logging
import pandas as pd  # Import pandas for data manipulation and CSV generation
import io  # Import io for handling in-memory file-like objects
from fastapi.responses import StreamingResponse  # Import StreamingResponse for streaming file responses
from typing import List, Optional  # Import type hints for optional and list types

class CandidateService:
    @staticmethod
    def create_candidate(candidate: Candidate, user_id: str) -> dict:
        """
        Create a new candidate and associate it with a user.
        
        - **candidate**: Candidate data for creation (validated with Candidate model)
        - **user_id**: ID of the user creating the candidate
        
        Returns:
        - A dictionary containing the status of the operation and the created candidate data.
        
        Raises:
        - HTTPException with status code 500 if an error occurs during candidate creation.
        """
        candidate.user_id = user_id
        try:
            candidate_data = CandidateRepository.create_candidate(candidate)
            return {"status": "success", "candidate": candidate_data}
        except Exception as e:
            logging.error(f"An error occurred while creating a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    @staticmethod
    def get_candidate(candidate_id: str, user_id: str) -> dict:
        """
        Retrieve a candidate by their ID.
        
        - **candidate_id**: ID of the candidate to retrieve
        - **user_id**: ID of the user requesting the candidate
        
        Returns:
        - The candidate data if found.
        
        Raises:
        - HTTPException with status code 404 if the candidate is not found.
        """
        candidate_data = CandidateRepository.get_candidate(candidate_id, user_id)
        if candidate_data:
            return candidate_data
        raise HTTPException(status_code=404, detail="Candidate not found")

    @staticmethod
    def edit_candidate(candidate_id: str, updated_candidate: Candidate, user_id: str) -> dict:
        """
        Update an existing candidate's information.
        
        - **candidate_id**: ID of the candidate to update
        - **updated_candidate**: New candidate data (validated with Candidate model)
        - **user_id**: ID of the user making the update
        
        Returns:
        - A dictionary containing the status of the operation and the updated candidate data.
        
        Raises:
        - HTTPException with status code 500 if an error occurs during candidate update.
        """
        try:
            updated_candidate_data = CandidateRepository.edit_candidate(candidate_id, updated_candidate, user_id)
            return {"status": "success", "candidate": updated_candidate_data}
        except Exception as e:
            logging.error(f"An error occurred while updating a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def delete_candidate(candidate_id: str, user_id: str) -> dict:
        """
        Delete a candidate by their ID.
        
        - **candidate_id**: ID of the candidate to delete
        - **user_id**: ID of the user requesting the deletion
        
        Returns:
        - A dictionary indicating the success of the deletion operation.
        
        Raises:
        - HTTPException with status code 500 if an error occurs during candidate deletion.
        """
        try:
            return CandidateRepository.delete_candidate(candidate_id, user_id)
        except Exception as e:
            logging.error(f"An error occurred while deleting a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def get_all_candidates(
        user_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        career_level: Optional[str] = None,
        job_major: Optional[str] = None,
        years_of_experience: Optional[int] = None,
        degree_type: Optional[str] = None,
        skills: Optional[List[str]] = None,
        nationality: Optional[str] = None,
        city: Optional[str] = None,
        salary_min: Optional[float] = None,
        salary_max: Optional[float] = None,
        gender: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[dict]:
        """
        Retrieve all candidates with optional filters.
        
        Returns:
        - A list of candidates matching the filters.
        
        Raises:
        - HTTPException with status code 404 if no candidates are found.
        - HTTPException with status code 500 if an error occurs during candidate retrieval.
        """
        filters = {}
        if first_name:
            filters["first_name"] = first_name
        if last_name:
            filters["last_name"] = last_name
        if email:
            filters["email"] = email
        if career_level:
            filters["career_level"] = career_level
        if job_major:
            filters["job_major"] = job_major
        if years_of_experience is not None:
            filters["years_of_experience"] = years_of_experience
        if degree_type:
            filters["degree_type"] = degree_type
        if skills:
            filters["skills"] = {"$in": skills}
        if nationality:
            filters["nationality"] = nationality
        if city:
            filters["city"] = city
        if salary_min is not None and salary_max is not None:
            filters["salary"] = {"$gte": salary_min, "$lte": salary_max}
        elif salary_min is not None:
            filters["salary"] = {"$gte": salary_min}
        elif salary_max is not None:
            filters["salary"] = {"$lte": salary_max}
        if gender:
            filters["gender"] = gender
        if search:
            filters["$text"] = {"$search": search}

        try:
            candidates = CandidateRepository.get_all_candidates(user_id, filters)
            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found")
            return candidates
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")

    @staticmethod
    def generate_report() -> StreamingResponse:
        """
        Generate a CSV report of all candidates.
        
        Returns:
        - A StreamingResponse containing the CSV file.
        
        Raises:
        - HTTPException with status code 404 if no candidates are found.
        - HTTPException with status code 500 if an error occurs during report generation.
        """
        try:
            candidates = CandidateRepository.fetch_all_candidates()
            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found")

            df = pd.DataFrame(candidates)
            df["_id"] = df["_id"].astype(str)

            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            return StreamingResponse(
                csv_buffer,
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=candidates_report.csv"}
            )
        except Exception as e:
            logging.error(f"An error occurred while generating the report: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
