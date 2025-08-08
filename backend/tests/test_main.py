from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_fix_grammar():
    response = client.post("/fix-grammar", json={"text": "he go to school.", "tone": "default"})
    assert response.status_code == 200
    assert "goes to school" in response.json()["corrected"].lower()
