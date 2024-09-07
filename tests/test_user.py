import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
    assert response.json()["email"] == "john.doe@example.com"

def test_get_user():
    response = client.get("/user")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of users