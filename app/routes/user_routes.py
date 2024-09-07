# Import necessary libraries and modules
from fastapi import APIRouter, Depends  # FastAPI components for routing and dependency injection
from app.models.user import User  # Import User model for request validation
from app.service.user_service import UserService  # Import UserService to handle user-related operations

# Create an APIRouter instance for routing user-related endpoints
user = APIRouter()

# Route to create a new user
@user.post("/user")
def create_user(user: User):
    """
    Create a new user.
    
    - **user**: User data for creation (validated with User model)
    
    Returns:
    - Response from UserService.create_user method
    """
    return UserService.create_user(user)

# Route to retrieve a user by their ID
@user.get("/user/{user_id}")
def get_user(user_id: str):
    """
    Retrieve a user by their ID.
    
    - **user_id**: ID of the user to retrieve
    
    Returns:
    - Response from UserService.get_user method
    """
    return UserService.get_user(user_id)
