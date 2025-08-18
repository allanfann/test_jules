import pytest
from fastapi.testclient import TestClient

# Import the FastAPI app instance
from app.main import app


@pytest.fixture(scope="module")
def client():
    """
    A pytest fixture to provide a TestClient for the API.
    `scope="module"` means the client is created once per test module.
    """
    # This will also trigger the lifespan events, loading the model.
    with TestClient(app) as c:
        yield c


# --- Test Cases for Legacy Endpoints ---


def test_text_processing_with_bert(client):
    """Test the /text-processing endpoint with the new BERT implementation."""
    # 1. Define request payload
    payload = {"text": "我愛北京天安門", "tenant_id": "test"}

    # 2. Send request
    response = client.post("/api/v1/legacy/text-processing", json=payload)

    # 3. Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Text processed successfully with BERT."
    assert data["data"]["original_text"] == "我愛北京天安門"

    # Check for BERT specific tokens
    assert "tokens" in data["data"]
    assert data["data"]["tokens"][0] == "[CLS]"
    assert data["data"]["tokens"][-1] == "[SEP]"

    # Check the embedding vector
    assert "embedding_vector" in data["data"]
    assert isinstance(data["data"]["embedding_vector"], list)
    assert (
        len(data["data"]["embedding_vector"]) == 768
    )  # bert-base-chinese has 768 dimensions


def test_information_extraction_with_bert(client):
    """Test the /information-extraction endpoint with the new BERT implementation."""
    payload = {"text": "張三昨天去了台北車站。", "tenant_id": "test"}
    response = client.post("/api/v1/legacy/information-extraction", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Information extracted using BERT tokenizer."

    # Check that entities are now BERT tokens
    assert "entities" in data["data"]
    assert data["data"]["entities"][0] == "[CLS]"
    assert "張" in data["data"]["entities"]
    assert "三" in data["data"]["entities"]
    assert "台" in data["data"]["entities"]
    assert "北" in data["data"]["entities"]

    # Check that events are empty as per the new implementation
    assert "events" in data["data"]
    assert data["data"]["events"] == []


def test_intent_classification_greeting(client):
    """Test the /intent-classification endpoint for a greeting (unchanged)."""
    payload = {"text": "你好啊，朋友！", "tenant_id": "test"}
    response = client.post("/api/v1/legacy/intent-classification", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["intent"] == "greeting"
    assert data["data"]["confidence"] == 1.0


def test_intent_classification_unknown(client):
    """Test the /intent-classification endpoint for an unknown intent (unchanged)."""
    payload = {"text": "這句話沒有特定意圖。", "tenant_id": "test"}
    response = client.post("/api/v1/legacy/intent-classification", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["intent"] == "Unknown"
    assert data["data"]["confidence"] == 0.0


def test_structured_conversion(client):
    """Test the /structured-conversion endpoint (unchanged)."""
    payload = {
        "text": "姓名: 王小明\n年齡 是 25",
        "tenant_id": "test",
        "schema_id": "user_info",
    }
    response = client.post("/api/v1/legacy/structured-conversion", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["schema_id"] == "user_info"
    assert "data" in data["data"]
    assert data["data"]["data"]["姓名"] == "王小明"
    assert data["data"]["data"]["年齡"] == "25"
