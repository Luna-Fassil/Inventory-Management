#imports 
import pytest
import tempfile
import os
import json
from inventory import FlaskApp, UserManager

@pytest.fixture
def client():
    flask_app = FlaskApp()
    app = flask_app.app
    app.testing = True
    return app.test_client()

#UT-01: Add Item - Valid Input
def test_add_item_valid(client):
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]
    response = client.post("/api/inventory/add", json={
        "token": token,  # valid token 
        "name": "Shirt",
        "quantity": 5,
        "price": 100,
        "color": "red",
        "brand": "nike",
        "season": "fall"
    })
    assert response.status_code == 201
    assert "Item added successfully" in response.get_json().get("message", "")

#UT-02: Remove Item - Valid ID
def test_remove_item_valid(client):
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]
    add_response = client.post("/api/inventory/add", json={
        "token": token,
        "name": "Temp",
        "quantity": 1,
        "price": 10,
        "color": "blue",
        "brand": "adidas",
        "season": "summer"
    })
    item_id = add_response.get_json()["item"]["id"]
    response = client.delete("/api/inventory/remove", json={
        "token": token,
        "id": item_id

    })
    assert response.status_code == 200
    assert "removed successfully" in response.get_json().get("message", "")

#UT-03: Add User - Writes to Temp File
def test_add_user_tempfile():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    try:
        user_manager = UserManager()
        user_manager.storage_path = path  #override to temp path

        response, status = user_manager.add_user({
            "username": "testuser",
            "email": "test@example.com",
            "password": "123",
            "role": "employee"
        })

        assert status == 201
        assert response["user"]["email"] == "test@example.com"

        #check file written correctly
        with open(path, "r") as f:
            data = json.load(f)
            assert any(u["email"] == "test@example.com" for u in data["users"])
    finally:
        os.remove(path)

#UT-04: Verify Session - Valid Token
def test_verify_session():
    flask_app = FlaskApp()
    token = flask_app.user_manager.login("admin", "password")[0]["token"]
    role = flask_app.user_manager.verify_session(token)
    assert role == "admin"

#UT-05: Login - Correct Credentials
def test_login_success(client):
    response = client.post("/api/login?username=admin&password=password")
    assert response.status_code == 200
    assert "token" in response.get_json()
    assert response.get_json()["role"] == "admin"

#UT-06: Add Item - Invalid Data
def test_add_item_invalid(client):
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]
    response = client.post("/api/inventory/add", json={
        "token": token,
        "name": "Bad",
        "quantity": -1,
        "price": 100,
        "color": "red",
        "brand": "puma",
        "season": "winter"
    })
    assert response.status_code == 400
    assert "Quantity must be non-negative" in response.get_json().get("error", "")
