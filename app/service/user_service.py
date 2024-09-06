from app.repository.user_repository import UserRepository
from app.models.user import User
from fastapi import HTTPException, status
import logging
from app.helper.token_helper import TokenHelper

class UserService:
    @staticmethod
    def create_user(user: User) -> dict:
        try:
            user_data = UserRepository.create_user(user)
            access_token = TokenHelper.create_access_token(
                data={"id": str(user_data["_id"])}
            )
            return {
                "status": "ok",
                "token": access_token,
                "user": user_data,
            }
        except Exception as e:
            logging.error(f"An error occurred while creating a user: {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    @staticmethod
    def get_user(user_id: str) -> dict:
        user_data = UserRepository.get_user(user_id)
        if user_data:
            return user_data
        raise HTTPException(status_code=404, detail="User not found")
