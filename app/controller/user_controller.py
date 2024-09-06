from app.config.db_config import user_collection
# from bson.objectid import ObjectId
from app.dtos.user_dto import User
from uuid import uuid4

class UserController:
    def create_user(user: User):
        user_data = user.dict()
        if user_data.get("UUID") is None:
            user_data["UUID"] = str(uuid4())
        
        result = user_collection.insert_one(user_data)
        if result.inserted_id:
            return user_data
        raise HTTPException(status_code=500, detail="User could not be created")
    
    # def read_user(user_id: str):
    #     user = user_collection.find_one({"_id": ObjectId(user_id)})
    #     if user:
    #         return user
    #     raise HTTPException(status_code=404, detail="User not found")