def test_create_content(auth_client):
    response = auth_client.post("/content/", json={
        "title": "Test Content",
        "body": "This is a test content."
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Create Content"

def test_get_content(auth_client):
    response = auth_client.get("/content/1")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Content"

def test_update_content(auth_client):
    response = auth_client.put("/content/1", json={
        "title": "Updated Content",
        "body": "Updated content body."
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Content"

def test_delete_content(auth_client):
    response = auth_client.delete("/content/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Content deleted successfully"}
