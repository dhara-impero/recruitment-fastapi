# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from app.routes.user_routes import user
from app.routes.candidate_routes import candidate
from app.helper.logger_helper import setup_logger
from pymongo import MongoClient
import os
import logging
from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

# setup_logger()

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

app.include_router(user)
app.include_router(candidate)
