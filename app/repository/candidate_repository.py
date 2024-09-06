from app.config.db_config import candidate_collection
from app.models.candidate import Candidate
from bson import ObjectId
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from typing import Optional, List

class CandidateRepository:
    @staticmethod
    def create_candidate(candidate: Candidate) -> dict:
        candidate_data = candidate.dict()
        result: InsertOneResult = candidate_collection.insert_one(candidate_data)
        if result.acknowledged:
            candidate_data["_id"] = str(result.inserted_id)
            return candidate_data
        raise Exception("Candidate could not be created")

    @staticmethod
    def get_candidate(candidate_id: str, user_id: str) -> Optional[dict]:
        candidate_data = candidate_collection.find_one({"_id": ObjectId(candidate_id), "user_id": user_id})
        if candidate_data:
            candidate_data["_id"] = str(candidate_data["_id"])
            return candidate_data
        return None

    @staticmethod
    def edit_candidate(candidate_id: str, updated_candidate: Candidate, user_id: str) -> dict:
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
        result: DeleteResult = candidate_collection.delete_one({"_id": ObjectId(candidate_id), "user_id": user_id})
        if result.deleted_count == 0:
            raise Exception("Candidate not found")
        return {"status": "success", "message": "Candidate deleted"}

    @staticmethod
    def get_all_candidates(user_id: str, filters: dict) -> List[dict]:
        query = {"user_id": user_id}
        query.update(filters)
        candidates_cursor = candidate_collection.find(query)
        candidates = list(candidates_cursor)
        for candidate in candidates:
            candidate["_id"] = str(candidate["_id"])
        return candidates

    @staticmethod
    def fetch_all_candidates() -> List[dict]:
        candidates_cursor = candidate_collection.find()
        candidates = list(candidates_cursor)
        return candidates
