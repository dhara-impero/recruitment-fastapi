# Import necessary libraries and modules
from app.repository.user_repository import UserRepository  # Import UserRepository for database operations
from app.models.user import User  # Import User model for type hinting and validation
from fastapi import HTTPException, status  # Import FastAPI components for handling HTTP exceptions
import logging  # Import logging for error logging
from app.helper.token_helper import TokenHelper  # Import TokenHelper for JWT token operations

class UserService:
    @staticmethod
    def create_user(user: User) -> dict:
        """
        Create a new user and generate an access token.
        
        - **user**: User data for creation (validated with User model)
        
        Returns:
        - A dictionary containing the status of the operation, an access token, and the created user data.
        
        Raises:
        - HTTPException with status code 500 if an error occurs during user creation.
        """
        
        try:
            # Attempt to create a user in the database
            user_data = UserRepository.create_user(user)
            
            # Generate an access token for the created user
            access_token = TokenHelper.create_access_token(
                data={"id": str(user_data["_id"])}
            )
            
            # Return a success response with the token and user data
            return {
                "status": "success",
                "token": access_token,
                "user": user_data,
            }
        except Exception as e:
            # Log any errors that occur during user creation
            logging.error(f"An error occurred while creating a user: {e}")
            
            # Raise an HTTPException with status code 500 for internal server errors
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    @staticmethod
    def get_user(user_id: str) -> dict:
        """
        Retrieve a user by their ID.
        
        - **user_id**: ID of the user to retrieve
        
        Returns:
        - User data if found.
        
        Raises:
        - HTTPException with status code 404 if the user is not found.
        """
        # Attempt to retrieve the user from the database
        user_data = UserRepository.get_user(user_id)
        
        if user_data:
            # Return the user data if found
            return user_data
        
        # Raise an HTTPException with status code 404 if the user is not found
        raise HTTPException(status_code=404, detail="User not found")
