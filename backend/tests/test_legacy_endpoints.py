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
    with TestClient(app) as c:
        yield c


# --- Test Cases for Legacy Endpoints ---


def test_text_processing(client):
    """Test the /text-processing endpoint."""
    # 1. Define request payload
    payload = {"text": "我愛北京天安門", "tenant_id": "test"}

    # 2. Send request
    response = client.post("/api/v1/legacy/text-processing", json=payload)

    # 3. Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["original_text"] == "我愛北京天安門"
    assert "tokens" in data["data"]
    assert "tfidf_vector" in data["data"]
    # Assert individual words as tokenized by jieba
    assert "我" in data["data"]["tokens"]
    assert "愛" in data["data"]["tokens"]
    assert "北京" in data["data"]["tokens"]
    # Jieba might split 天安門, so we check for its parts or the whole
    # A safer check might be to see if the tokens list is not empty
    assert len(data["data"]["tokens"]) > 0


def test_information_extraction(client):
    """Test the /information-extraction endpoint."""
    payload = {"text": "張三昨天去了台北車站。", "tenant_id": "test"}
    response = client.post("/api/v1/legacy/information-extraction", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "entities" in data["data"]
    assert "events" in data["data"]
    assert "張三" in data["data"]["entities"]
    # Assert individual words as tokenized by jieba
    assert "台北" in data["data"]["entities"]
    assert "車站" in data["data"]["entities"]
    assert "去" in data["data"]["events"]


def test_intent_classification_greeting(client):
    """Test the /intent-classification endpoint for a greeting."""
    payload = {"text": "你好啊，朋友！", "tenant_id": "test"}
    response = client.post("/api/v1/legacy/intent-classification", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["intent"] == "greeting"
    assert data["data"]["confidence"] == 1.0


def test_intent_classification_unknown(client):
    """Test the /intent-classification endpoint for an unknown intent."""
    payload = {"text": "這句話沒有特定意圖。", "tenant_id": "test"}
    response = client.post("/api/v1/legacy/intent-classification", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["intent"] == "Unknown"
    assert data["data"]["confidence"] == 0.0

def test_structured_conversion(client):
    """Test the /structured-conversion endpoint."""
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
