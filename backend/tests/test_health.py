from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/saude")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "operacional"
    assert "version" in data
    assert "env" in data
