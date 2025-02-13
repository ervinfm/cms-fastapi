import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.main import app
from fastapi.testclient import TestClient

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def auth_client(client):
    """Menghasilkan client dengan token otentikasi"""
    # Registrasi user untuk login (jika perlu)
    client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })

    # Login dan ambil token
    response = client.post("/token", data={
        "username": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200
    token = response.json().get("access_token")

    # Tambahkan token ke headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
