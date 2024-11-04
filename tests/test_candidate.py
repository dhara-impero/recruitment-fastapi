from fastapi.testclient import TestClient
from app.main import app
from app.helper.token_helper import TokenHelper  # Import the TokenHelper for token generation

# Initialize the TestClient for testing the FastAPI app
client = TestClient(app)

# Sample data to use in tests
sample_candidate = {
    "first_name": "John",  # Candidate's first name
    "last_name": "Doe",    # Candidate's last name
    "email": "john.doe@example.com",  # Candidate's email address
    "uuid": "test-uuid",  # Unique identifier for the candidate
    "career_level": "Mid",  # Career level of the candidate
    "job_major": "Software Engineering",  # Major or field of study
    "years_of_experience": 5,  # Number of years of experience
    "degree_type": "Bachelor",  # Type of degree obtained
    "skills": ["Python", "FastAPI"],  # List of skills
    "nationality": "American",  # Nationality of the candidate
    "city": "New York",  # City where the candidate resides
    "salary": 80000,  # Expected salary
    "gender": "Male"  # Gender of the candidate
}

# Create an access token for authorization using TokenHelper
token = TokenHelper.create_access_token(sample_candidate)

def test_create_candidate() -> None:
    """
    Test the candidate creation endpoint with valid data.
    """
    # Send a POST request to create a candidate with sample data
    response = client.post("/candidate", json=sample_candidate, headers={"Authorization": f"Bearer {token}"})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response JSON contains success status
    assert response.json()["status"] == "success"
    
    # Assert that the created candidate's first name matches the sample data
    assert response.json()["candidate"]["first_name"] == sample_candidate["first_name"]

def test_get_all_candidates() -> None:
    """
    Test the endpoint for retrieving all candidates.
    """
    # Send a GET request to retrieve all candidates
    response = client.get("/all-candidates", headers={"Authorization": f"Bearer {token}"})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response is a list
    assert isinstance(response.json(), list)

def test_generate_report() -> None:
    """
    Test the endpoint for generating a report.
    """
    # Send a GET request to generate a report
    response = client.get("/generate-report", headers={"Authorization": f"Bearer {token}"})
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the content type of the response is CSV
    assert response.headers["Content-Type"] == "text/csv; charset=utf-8"

def test_create_candidate_invalid_data() -> None:
    """
    Test candidate creation with invalid data (e.g., invalid email format).
    """
    # Modify sample data to include invalid email
    invalid_candidate = sample_candidate.copy()
    invalid_candidate["email"] = "invalid-email"  # Invalid email format
    
    # Send a POST request to create a candidate with invalid data
    response = client.post("/candidate", json=invalid_candidate, headers={"Authorization": f"Bearer {token}"})
    
    # Assert that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422
