# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI()

# Health check route
@app.get("/health", status_code=200)
def health_check():
    """
    Health check endpoint to verify that the server is running.
    """
    return {"status": "healthy"}

# Other routes and logic here...

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8989)
