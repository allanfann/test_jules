import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app instance
from app.main import app


@pytest.fixture(scope="module")
def client():
    """
    A pytest fixture to provide a TestClient for the API.
    """
    with TestClient(app) as c:
        yield c


# --- Test Cases for Analysis Endpoints ---

def test_personality_analysis(client):
    """Test the /personality_analysis endpoint."""
    payload = {"text": "I am an optimist."}
    response = client.post("/api/v1/analysis/personality_analysis", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "personality" in data
    assert "scores" in data


def test_mbti_analysis(client):
    """Test the /mbti_analysis endpoint."""
    payload = {"answers": ["E", "N", "F", "P"]}
    response = client.post("/api/v1/analysis/mbti_analysis", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mbti_type"] == "ENFP"
    assert "summary" in data
    assert "description" in data

def test_mbti_analysis_invalid(client):
    """Test the /mbti_analysis endpoint with invalid input."""
    payload = {"answers": ["E", "N"]}
    response = client.post("/api/v1/analysis/mbti_analysis", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
