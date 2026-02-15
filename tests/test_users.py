from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "name": "John",
        "email": "john@example.com",
        "role": "student"
    })
    assert response.status_code == 200
