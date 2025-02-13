from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_user():
    response = client.post("/token", json={
        "email": "test@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
