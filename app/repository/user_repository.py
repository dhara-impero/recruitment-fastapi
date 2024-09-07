from app.config.db_config import user_collection
from app.models.user import User
from bson import ObjectId
from pymongo.results import InsertOneResult
from typing import Optional

class UserRepository:
    @staticmethod
    def create_user(user: User) -> dict:
        user_data = user.__dict__  # Convert Pydantic model to dict
        result: InsertOneResult = user_collection.insert_one(user_data)
        if result.acknowledged:
            user_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
            return user_data
        raise Exception("User could not be created")
    
    @staticmethod
    def get_user(user_id: str) -> Optional[dict]:
        user_data = user_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            user_data["_id"] = str(user_data["_id"])  # Convert ObjectId to string
            return user_data
        return None
