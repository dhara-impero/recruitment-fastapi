from fastapi import APIRouter, Depends
from app.dtos.user_dto import User
from app.controller.user_controller import UserController

user = APIRouter()

@user.post("/user")
def create_user(user: User):
    return UserController.create_user(user)

# Add more routes for update, delete, etc.