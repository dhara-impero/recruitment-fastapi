from app.config.db_config import user_collection
# from bson.objectid import ObjectId
from app.dtos.user_dto import User
from uuid import uuid4
from fastapi import HTTPException, status
import logging
from bson import ObjectId


class UserController:
    def create_user(user: User):
        user_data = user.dict()  # Convert Pydantic model to dict
        try:
            # Insert user data into the MongoDB collection
            result: InsertOneResult = user_collection.insert_one(user_data)

            # Check if the insertion was successful
            if result.acknowledged:
                # Return user data along with the created ID
                user_data["_id"] = str(result.inserted_id)  # Convert ObjectId to string
                return {"status": "success", "user": user_data}

            # If not acknowledged, raise an exception
            raise HTTPException(status_code=500, detail="User could not be created")

        except Exception as e:
            # Log the error for debugging purposes
            logging.error(f"An error occurred while creating a user: {e}")
            # Raise an HTTPException with a 500 status code
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    
    def get_user(user_id: str):
        try:
            # Query the MongoDB collection for the user with the given ID
            user_data = user_collection.find_one({"_id": ObjectId(user_id)})
            
            # Check if user data was found
            if user_data is None:
                raise HTTPException(status_code=404, detail="User not found")
            
            # Convert ObjectId to string if needed
            user_data["_id"] = str(user_data["_id"])
            
            return user_data
        
        except Exception as e:
            # Log the error for debugging purposes
            logging.error(f"An error occurred while retrieving a user: {e}")
            # Raise an HTTPException with a 500 status code
            raise HTTPException(status_code=500, detail="Internal Server Error")
    