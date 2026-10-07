from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/users/", json={"name": "test", "email": "test@test.com"})
    # It will fail because we intentionally throw Exception
    assert response.status_code == 500

def test_update_profile():
    response = client.post("/users/profile", json={"id": 1, "settings": None})
    # It will fail because of missing null-check
    assert response.status_code == 500
