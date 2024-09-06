from fastapi import APIRouter, Depends
from app.dtos.user_dto import User
from app.controller.user_controller import UserController

user = APIRouter()

@user.post("/user")
def create_user(user: User):
    return UserController.create_user(user)

@user.get("/user/{user_id}")
def get_user(user_id: str):
    return UserController.get_user(user_id)
