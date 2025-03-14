import pytest
import json
from inventory import app  # import app form inventory file

@pytest.fixture
def client():
    print("Creates a test client for  Flask")
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    print("Test if the home page loads correctly")
    response = client.get("/")
    assert response.status_code == 200
    print("home page loaded")

def test_get_empty_inventory(client):
    print("Test retrieving inventory when it's empty")
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.json == []  #initially empty inventory

def test_add_item(client):
    print("Test adding an item to the inventory")
    item_data = {
        "name": "Shirt",
        "quantity": 10,
        "price": 200,
        "color": "Green",
    }
    response = client.post("/add", json=item_data)
    print("adding item - Name: Shirt, Quantity: 10, Price: 200, Color: Green")
    
    assert response.status_code == 201
    data = response.json
    assert data["message"] == "Item added successfully"
    assert data["item"]["name"] == "Shirt"
    assert data["item"]["quantity"] == 10
    assert data["item"]["price"] == 200
    assert data["item"]["color"] == "Green"

def test_get_inventory(client):
    print("Test retrieving inventory with one item")
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.json) == 1  #inventory should have 1 item

def test_remove_item(client):
    print("Test removing an item from inventory")
    item_id = 0  #assume it has id 0
    response = client.delete("/remove", json={"id": item_id})
    assert response.status_code == 200
    assert response.json["message"] == f"Item with ID {item_id} removed successfully"

def test_remove_nonexistent_item(client):
    print("Test removing an item that does not exist")
    response = client.delete("/remove", json={"id": 999})  #id that doesnt exist
    assert response.status_code == 404
    assert response.json["error"] == "Item not found"

def test_edit_item(client):
    print("Test editing an item in inventory")
    #add an item to edit
    item_data = {
        "name": "Sweater",
        "quantity": 53,
        "price": 500,
        "color": "Yellow",
    }
    client.post("/add", json=item_data)

    #edit item
    edit_data = {
        "id": 1,  #ID 1
        "name": "Dress",
        "quantity": 8,
        "price": 700,
        "color": "Blue",
    }
    response = client.post("/edit", json=edit_data)

    assert response.status_code == 200
    assert response.json["item"]["name"] == "Dress"
    assert response.json["item"]["quantity"] == 8
    assert response.json["item"]["price"] == 700
    assert response.json["item"]["color"] == "Blue"

def test_edit_nonexistent_item(client):
    print("Test editing an item that does not exist")
    response = client.post("/edit", json={"id": 999, "name": "Fake", "quantity": 1, "price": 10, "color": "Red"})
    assert response.status_code == 404
    assert response.json["error"] == "Item not found"
