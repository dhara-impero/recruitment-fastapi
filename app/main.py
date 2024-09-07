# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from app.routes.user_routes import user
from app.routes.candidate_routes import candidate
from app.helper.logger_helper import setup_logger
import os
import logging
from dotenv import load_dotenv
from os.path import join, dirname

# Load environment variables from the .env file
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

setup_logger()

# Create the FastAPI application instance
app = FastAPI(
    title="FastAPI",
    version="0.0.1",
)
    
# Health check route
@app.get("/health", status_code=200)
def health_check():
    """
    Health check endpoint to verify that the server is running.
    """
    return {"status": "healthy"}

# Include routers for user and candidate endpoints
app.include_router(user)  # Register the user router for user-related routes
app.include_router(candidate)  # Register the candidate router for candidate-related routes


