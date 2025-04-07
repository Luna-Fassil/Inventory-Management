# imports 
import pytest
import tempfile
import os
import json
from inventory import FlaskApp, UserManager

@pytest.fixture
def client():
    # create and return flask test client
    flask_app = FlaskApp()
    app = flask_app.app
    app.testing = True
    return app.test_client()

# UT-01: Add Item - Valid Input
def test_add_item_valid(client):
    # login to get token
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]

    # send valid add request
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

# UT-02: Remove Item - Valid ID
def test_remove_item_valid(client):
    # login to get token
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]

    # add item to remove
    add_response = client.post("/api/inventory/add", json={
        "token": token,
        "name": "Temp",
        "quantity": 1,
        "price": 10,
        "color": "blue",
        "brand": "adidas",
        "season": "summer"
    })

    # get id of the added item
    item_id = add_response.get_json()["item"]["id"]

    # send remove request
    response = client.delete("/api/inventory/remove", json={
        "token": token,
        "id": item_id
    })
    assert response.status_code == 200
    assert "removed successfully" in response.get_json().get("message", "")

# UT-03: Add User - Writes to Temp File
def test_add_user_tempfile():
    # create temp file for isolated user data
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        path = tmp.name
    try:
        user_manager = UserManager()
        user_manager.storage_path = path  # override to temp path

        # add new user
        response, status = user_manager.add_user({
            "username": "testuser",
            "email": "test@example.com",
            "password": "123",
            "role": "employee"
        })

        assert status == 201
        assert response["user"]["email"] == "test@example.com"

        # check if user was saved in temp file
        with open(path, "r") as f:
            data = json.load(f)
            assert any(u["email"] == "test@example.com" for u in data["users"])
    finally:
        os.remove(path)  # cleanup temp file

# UT-04: Verify Session - Valid Token
def test_verify_session():
    # create app and login to get token
    flask_app = FlaskApp()
    token = flask_app.user_manager.login("admin", "password")[0]["token"]

    # verify session using token
    role = flask_app.user_manager.verify_session(token)
    assert role == "admin"

# UT-05: Login - Correct Credentials
def test_login_success(client):
    # test login with correct credentials
    response = client.post("/api/login?username=admin&password=password")
    assert response.status_code == 200
    assert "token" in response.get_json()
    assert response.get_json()["role"] == "admin"

# UT-06: Add Item - Invalid Data
def test_add_item_invalid(client):
    # login to get token
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]

    # try to add item with invalid quantity
    response = client.post("/api/inventory/add", json={
        "token": token,
        "name": "Bad",
        "quantity": -1,  # invalid quantity
        "price": 100,
        "color": "red",
        "brand": "puma",
        "season": "winter"
    })
    assert response.status_code == 400
    assert "Quantity must be non-negative" in response.get_json().get("error", "")

