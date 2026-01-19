import base64
import os

from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


def test_image_json_mock_provider():
    os.environ["PROVIDER"] = "mock"
    get_settings.cache_clear()
    client = TestClient(app)

    payload = {
        "image_base64": base64.b64encode(b"fake-image-bytes").decode("ascii"),
        "prompt": "extract text",
        "upload_to_memos": False,
    }
    response = client.post("/v1/image/json", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "URL:" in data["llm"]["markdown"]
