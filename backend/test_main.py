from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test 1 - Check if server is running
def test_root():
    response = client.get("/")
    assert response.status_code == 200

# Test 2 - Check if generate endpoint works
def test_generate():
    response = client.post("/generate", json={
        "story": "As a user I want to login so that I can access my account"
    })
    assert response.status_code == 200

# Test 3 - Check if empty story is handled
def test_empty_story():
    response = client.post("/generate", json={
        "story": ""
    })
    assert response.status_code == 200

# Test 4 - Check download endpoint exists
def test_download():
    response = client.get("/download")
    assert response.status_code == 200