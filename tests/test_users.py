def test_get_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_update_user(client):
    response = client.put("/users/1", json={
        "username": "updated_user",
        "email": "updated@example.com",
        "password": "newpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "updated_user"

def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
