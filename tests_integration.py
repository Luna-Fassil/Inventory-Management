# imports
import pytest
import json
from inventory import FlaskApp

@pytest.fixture
def client():
    # create flask test client
    flask_app = FlaskApp()
    app = flask_app.app
    app.testing = True
    return app.test_client()

# IT-01: Add item via API and check inventory.json updated
def test_add_item_updates_inventory_file(client):
    # login to get admin token
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]

    # add item to inventory
    response = client.post("/api/inventory/add", json={
        "token": token,
        "name": "TestItem",
        "quantity": 3,
        "price": 20,
        "color": "blue",
        "brand": "adidas",
        "season": "fall"
    })
    assert response.status_code == 201

    # check if item was written to file
    with open("data/inventory.json") as f:
        inventory = json.load(f)["inventory"]
        assert any(item["name"] == "TestItem" for item in inventory)

# IT-02: Add user via API and check users.json updated
def test_add_user_updates_users_file(client):
    # login as admin
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    login_data = login.get_json()
    token = login_data["token"]
    assert login_data["role"] == "admin"

    # create unique username using timestamp
    import time
    unique_username = f"testuser_{int(time.time())}"

    # add new user
    response = client.post("/api/users/add", json={
        "token": token,
        "username": unique_username,
        "email": f"{unique_username}@email.com",
        "password": "123",
        "role": "employee"
    })
    assert response.status_code == 201

    # check if user was saved in file
    with open("data/users.json") as f:
        users = json.load(f)["users"]
        expected_email = f"{unique_username}@email.com"
        assert any(user["email"] == expected_email for user in users)

# IT-03: Unauthorized add attempt by employee
def test_employee_cannot_add_item(client):
    # login as guest (non-admin)
    login = client.post("/api/login?username=guest&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]

    # try adding item as guest
    response = client.post("/api/inventory/add", json={
        "token": token,
        "name": "UnauthorizedItem",
        "quantity": 1,
        "price": 10,
        "color": "green",
        "brand": "nike",
        "season": "summer"
    })
    assert response.status_code == 401

# IT-04: Search for items with filter applied
def test_search_inventory_filter(client):
    # login as admin
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]

    # search with filter
    response = client.post("/api/inventory", json={
        "token": token,
        "filters": {"search": "s"},
        "amount": 10,
        "skip": 0
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

# IT-05: Delete item and confirm it is removed from inventory.json
def test_delete_item_updates_inventory_file(client):
    # login and add item
    login = client.post("/api/login?username=admin&password=password")
    assert login.status_code == 200
    token = login.get_json()["token"]

    add_response = client.post("/api/inventory/add", json={
        "token": token,
        "name": "DeleteMe",
        "quantity": 1,
        "price": 5,
        "color": "red",
        "brand": "nike",
        "season": "winter"
    })
    item_id = add_response.get_json()["item"]["id"]

    # delete the added item
    response = client.delete("/api/inventory/remove", json={
        "token": token,
        "id": item_id
    })
    assert response.status_code == 200

    # check if item is gone from file
    with open("data/inventory.json") as f:
        inventory = json.load(f)["inventory"]
        assert all(item["id"] != item_id for item in inventory)