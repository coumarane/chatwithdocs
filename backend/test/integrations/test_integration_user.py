from fastapi.testclient import TestClient
from app.main import app

from app.domain import User

client = TestClient(app)

def test_create_user():
    user = {
        "username": "helios1",
        "email": "helios@example.com",
        "password": "pass123"
    }
    response = client.post("/api/users", json=user)
    assert response.status_code == 200
    assert response.json() == user