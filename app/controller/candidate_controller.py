from app.config.db_config import user_collection, candidate_collection
from fastapi.responses import StreamingResponse
from app.dtos.user_dto import User
from app.dtos.candidate_dto import Candidate
from uuid import uuid4
from fastapi import HTTPException, status, Query
import logging
from bson import ObjectId
from typing import List, Optional, Literal
import pandas as pd
import io
from pymongo import MongoClient
from typing import List


class CandidateController:
    def create_candidate(candidate: Candidate):
        candidate_data = candidate.dict()  # Convert Pydantic model to dict
        try:
            # Insert user data into the MongoDB collection
            result: InsertOneResult = candidate_collection.insert_one(candidate_data)

            # Check if the insertion was successful
            if result.acknowledged:
                # Return user data along with the created ID
                candidate_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
                return {"status": "success", "candidate": candidate_data}

            # If not acknowledged, raise an exception
            raise HTTPException(status_code=500, detail="Candidate could not be created")

        except Exception as e:
            # Log the error for debugging purposes
            logging.error(f"An error occurred while creating a user: {e}")
            # Raise an HTTPException with a 500 status code
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    def get_candidate(candidate_id: str):
        try:
            print("candidate")
            candidate_data = candidate_collection.find_one({"_id": ObjectId(candidate_id)})
            if candidate_data is None:
                raise HTTPException(status_code=404, detail="Candidate not found")
            candidate_data["_id"] = str(candidate_data["_id"])
            return candidate_data
        except Exception as e:
            logging.error(f"An error occurred while retrieving a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def edit_candidate(candidate_id: str, updated_candidate: Candidate):
        print("*****")
        try:
            update_result: UpdateResult = candidate_collection.update_one(
                {"_id": ObjectId(candidate_id)},
                {"$set": updated_candidate.dict(exclude_unset=True)}
            )
            if update_result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Candidate not found")
            if update_result.modified_count == 0:
                raise HTTPException(status_code=400, detail="Candidate update failed")
            updated_candidate_data = candidate_collection.find_one({"_id": ObjectId(candidate_id)})
            updated_candidate_data["_id"] = str(updated_candidate_data["_id"])
            return {"status": "success", "candidate": updated_candidate_data}
        except Exception as e:
            logging.error(f"An error occurred while updating a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def delete_candidate(candidate_id: str):
        try:
            delete_result: DeleteResult = candidate_collection.delete_one({"_id": ObjectId(candidate_id)})
            if delete_result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Candidate not found")
            return {"status": "success", "message": "Candidate deleted"}
        except Exception as e:
            logging.error(f"An error occurred while deleting a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def get_all_candidates(
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
        try:
            query = {}
            if first_name:
                query["first_name"] = first_name
            if last_name:
                query["last_name"] = last_name
            if email:
                query["email"] = email
            if career_level:
                query["career_level"] = career_level
            if job_major:
                query["job_major"] = job_major
            if years_of_experience is not None:
                query["years_of_experience"] = years_of_experience
            if degree_type:
                query["degree_type"] = degree_type
            if skills:
                query["skills"] = {"$in": skills}
            if nationality:
                query["nationality"] = nationality
            if city:
                query["city"] = city
            if salary_min is not None and salary_max is not None:
                query["salary"] = {"$gte": salary_min, "$lte": salary_max}
            elif salary_min is not None:
                query["salary"] = {"$gte": salary_min}
            elif salary_max is not None:
                query["salary"] = {"$lte": salary_max}
            if gender:
                query["gender"] = gender
            if search:
                query["$text"] = {"$search": search}
            print("--------------------------------")
            print(query)
            candidates = list(candidate_collection.find({"$text": {"$search": "Dhara"}}))
            for candidate in candidates:
                candidate["_id"] = str(candidate["_id"])
            return candidates
        except Exception as e:
            logging.error(f"An error occurred while retrieving candidates: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        
    def generate_report():
        try:
            # Fetch all candidates
            candidates = list(candidate_collection.find())

            if not candidates:
                raise HTTPException(status_code=404, detail="No candidates found")

            # Convert candidates to DataFrame
            df = pd.DataFrame(candidates)
            
            # Convert ObjectId to string
            df["_id"] = df["_id"].astype(str)

            # Create a CSV in memory
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False)

            # Seek to the start of the stream
            csv_buffer.seek(0)

            return StreamingResponse(
                csv_buffer,
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=candidates_report.csv"}
            )

        except Exception as e:
            logging.error(f"An error occurred while generating the report: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    