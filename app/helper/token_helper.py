# Importing libraries
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, Header
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from app.config.db_config import user_collection
from bson import ObjectId
from app.dtos.user_dto import UserResponseModel
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user")

# JWT Configuration

"""Please generate a new JWT_SECRET `using openssl rand -hex 32` command and add it in the .env file"""

# Initializing the Hashing alogorith
JWT_SECRET = os.getenv('JWT_SECRET')
ALGORITHM = "HS256"

class TokenHelper:
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, JWT_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

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
