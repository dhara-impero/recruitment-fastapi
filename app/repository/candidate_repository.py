from app.config.db_config import candidate_collection
from app.models.candidate import Candidate
from bson import ObjectId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from typing import Optional, List

class CandidateRepository:
    @staticmethod
    def create_candidate(candidate: Candidate) -> dict:
        """
        Create a new candidate and insert it into the database.
        
        - **candidate**: Candidate data for creation (validated with Candidate model)
        
        Returns:
        - A dictionary containing the created candidate data with the generated ID.
        
        Raises:
        - Exception if the candidate could not be created.
        """
        candidate_data = candidate.__dict__
        result: InsertOneResult = candidate_collection.insert_one(candidate_data)
        if result.acknowledged:
            candidate_data["_id"] = str(result.inserted_id)
            return candidate_data
        raise Exception("Candidate could not be created")

    @staticmethod
    def get_candidate(candidate_id: str, user_id: str) -> Optional[dict]:
        """
        Retrieve a candidate by their ID and associated user ID.
        
        - **candidate_id**: ID of the candidate to retrieve
        - **user_id**: ID of the user associated with the candidate
        
        Returns:
        - The candidate data if found, otherwise None.
        """
        candidate_data = candidate_collection.find_one({"_id": ObjectId(candidate_id), "user_id": user_id})
        if candidate_data:
            candidate_data["_id"] = str(candidate_data["_id"])
            return candidate_data
        return None

    @staticmethod
    def edit_candidate(candidate_id: str, updated_candidate: Candidate, user_id: str) -> dict:
        """
        Update an existing candidate's information.
        
        - **candidate_id**: ID of the candidate to update
        - **updated_candidate**: New candidate data (validated with Candidate model)
        - **user_id**: ID of the user making the update
        
        Returns:
        - A dictionary containing the updated candidate data.
        
        Raises:
        - Exception if the candidate is not found or the update fails.
        """
        result: UpdateResult = candidate_collection.update_one(
            {"_id": ObjectId(candidate_id), "user_id": user_id},
            {"$set": updated_candidate.dict(exclude_unset=True)}
        )
        if result.matched_count == 0:
            raise Exception("Candidate not found")
        if result.modified_count == 0:
            raise Exception("Candidate update failed")
        updated_candidate_data = candidate_collection.find_one({"_id": ObjectId(candidate_id)})
        updated_candidate_data["_id"] = str(updated_candidate_data["_id"])
        return updated_candidate_data

    @staticmethod
    def delete_candidate(candidate_id: str, user_id: str) -> dict:
        """
        Delete a candidate by their ID and associated user ID.
        
        - **candidate_id**: ID of the candidate to delete
        - **user_id**: ID of the user associated with the candidate
        
        Returns:
        - A dictionary indicating the success of the deletion operation.
        
        Raises:
        - Exception if the candidate is not found.
        """
        result: DeleteResult = candidate_collection.delete_one({"_id": ObjectId(candidate_id), "user_id": user_id})
        if result.deleted_count == 0:
            raise Exception("Candidate not found")
        return {"status": "success", "message": "Candidate deleted"}

    @staticmethod
    def get_all_candidates(user_id: str, filters: dict) -> List[dict]:
        """
        Retrieve all candidates for a specific user with optional filters.
        
        - **user_id**: ID of the user requesting the candidates
        - **filters**: Dictionary of filter criteria for querying candidates
        
        Returns:
        - A list of candidates matching the filters.
        """
        query = {"user_id": user_id}
        query.update(filters)
        candidates_cursor = candidate_collection.find(query)
        candidates = list(candidates_cursor)
        for candidate in candidates:
            candidate["_id"] = str(candidate["_id"])
        return candidates

    @staticmethod
    def fetch_all_candidates() -> List[dict]:
        """
        Retrieve all candidates from the database.
        
        Returns:
        - A list of all candidates.
        """
        candidates_cursor = candidate_collection.find()
        candidates = list(candidates_cursor)
        return candidates
