from fastapi import HTTPException
from fastapi.testclient import TestClient
from app.main import app

# Initialize the TestClient for testing the FastAPI app
client = TestClient(app)

def test_create_user() -> None:
    """
    Test the user creation endpoint with valid data.
    """
    # Sample data to be used for creating a user
    user_data = {
        "first_name": "John",  # User's first name
        "last_name": "Doe",    # User's last name
        "email": "john.doe@example.com"  # User's email address
    }
    
    # Send a POST request to create a user with the sample data
    response = client.post("/user", json=user_data)
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response JSON contains the correct first name
    assert response.json()["user"]["first_name"] == "John"
    
    # Assert that the response JSON contains the correct email address
    assert response.json()["user"]["email"] == "john.doe@example.com"


def test_get_user():
    user_id ="66dc2845cd3a5ae7e6971508"
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 200