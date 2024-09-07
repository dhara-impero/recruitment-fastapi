# Importing libraries
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from app.config.db_config import user_collection
from bson import ObjectId
from app.models.user import UserResponseModel
from fastapi.security import OAuth2PasswordBearer

# Load environment variables from the .env file
load_dotenv()

# Initialize OAuth2PasswordBearer to use in dependency injection, for token authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user")

# JWT Configuration

"""Please generate a new JWT_SECRET `using openssl rand -hex 32` command and add it in the .env file"""

# Initialize the JWT secret and hashing algorithm from environment variables
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"

# TokenHelper class for managing JWT creation and verification
class TokenHelper:
    
    # Method for creating a new JWT access token
    def create_access_token(data: dict):
        to_encode = data.copy()  # Copy the input data to avoid modifying the original dictionary
        expire = datetime.utcnow() + timedelta(days=30)  # Set expiration time to 30 days from now
        to_encode.update({"exp": expire})  # Add expiration time to the payload
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)  # Encode the payload with the secret and algorithm
        return encoded_jwt  # Return the encoded JWT
    
    # Method for verifying the JWT token
    def verify_token(token: str = Depends(oauth2_scheme)) -> UserResponseModel:
        try:                      
            payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM]) 
            user_id: str = payload.get("id")
            if user_id is None:
                return {"message": "Unauthorized"}
        except JWTError:
            return {"message": "Unauthorized"}
        user = user_collection.find_one({"_id": ObjectId(user_id)}) 
        user["_id"] = str(user["_id"])
        if user is None: 
            return {"message": "Unauthorized"}
        return user
