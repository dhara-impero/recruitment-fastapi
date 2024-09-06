# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from app.routes.user_routes import user

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
