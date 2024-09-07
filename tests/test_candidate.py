import pytest
from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import io

client = TestClient(app)

# Sample data to use in tests
sample_candidate = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "uuid": "test-uuid",
    "career_level": "Mid",
    "job_major": "Software Engineering",
    "years_of_experience": 5,
    "degree_type": "Bachelor",
    "skills": ["Python", "FastAPI"],
    "nationality": "American",
    "city": "New York",
    "salary": 80000,
    "gender": "Male"
}

def test_create_candidate():
    response = client.post("/candidate", json=sample_candidate)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["candidate"]["first_name"] == sample_candidate["first_name"]

def test_get_all_candidates():
    response = client.get("/all-candidates")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_generate_report():
    response = client.get("/generate-report")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv"
    
    # Check if the content is a CSV
    content = response.content.decode("utf-8")
    assert "first_name" in content
    assert "last_name" in content

def test_create_candidate_invalid_data():
    invalid_candidate = sample_candidate.copy()
    invalid_candidate["email"] = "invalid-email"
    response = client.post("/candidates", json=invalid_candidate)
    assert response.status_code == 422  # Unprocessable Entity