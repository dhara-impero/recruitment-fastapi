from fastapi import APIRouter, Depends
from app.models.user import User
from app.service.user_service import UserService

user = APIRouter()

@user.post("/user")
def create_user(user: User):
    return UserService.create_user(user)

@user.get("/user/{user_id}")
def get_user(user_id: str):
    return UserService.get_user(user_id)
