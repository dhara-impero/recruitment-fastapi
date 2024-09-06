from app.config.db_config import user_collection,candidate_collection
from app.dtos.user_dto import User
from app.dtos.candidate_dto import Candidate
from uuid import uuid4
from fastapi import HTTPException, status
import logging

class CandidateController:
    def create_candidate(candidate: Candidate):
        print("candidate")
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
            candidate_data = CandidateController.candidate_collection.find_one({"_id": candidate_id})
            if candidate_data is None:
                raise HTTPException(status_code=404, detail="Candidate not found")
            candidate_data["_id"] = str(candidate_data["_id"])
            return candidate_data
        except Exception as e:
            logging.error(f"An error occurred while retrieving a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def update_candidate(candidate_id: str, updated_candidate: Candidate):
        try:
            update_result: UpdateResult = CandidateController.candidate_collection.update_one(
                {"_id": candidate_id},
                {"$set": updated_candidate.dict(exclude_unset=True)}
            )
            if update_result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Candidate not found")
            if update_result.modified_count == 0:
                raise HTTPException(status_code=400, detail="Candidate update failed")
            updated_candidate_data = CandidateController.candidate_collection.find_one({"_id": candidate_id})
            updated_candidate_data["_id"] = str(updated_candidate_data["_id"])
            return {"status": "success", "candidate": updated_candidate_data}
        except Exception as e:
            logging.error(f"An error occurred while updating a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")

    def delete_candidate(candidate_id: str):
        try:
            delete_result: DeleteResult = CandidateController.candidate_collection.delete_one({"_id": candidate_id})
            if delete_result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Candidate not found")
            return {"status": "success", "detail": "Candidate deleted"}
        except Exception as e:
            logging.error(f"An error occurred while deleting a candidate: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    