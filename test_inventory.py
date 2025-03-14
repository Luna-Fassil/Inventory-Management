import pytest
import json # so we can do json requests
from unittest.mock import patch #TO CREATE MOCK OBJECTS TO MOCK INVENTORU
from inventory import app  #import app from inventory file

@pytest.fixture #create flask test client
def client():
    print("Creates a test client for Flask")
    app.config["TESTING"] = True #enable testing
    with app.test_client() as client:
        yield client #provide client for all tests

def test_home(client):
    print("Test if the home page loads correctly")
    response = client.get("/") #simulates opening home page
    assert response.status_code == 200 #asserts success
    print("Home page loaded")

@patch("inventory.get_inventory", return_value=[])# mocks get inventoru
def test_get_empty_inventory(mock_get_inventory, client):
    print("Test retrieving inventory when it's empty")
    response = client.get("/inventory")
    assert response.status_code == 200 #asserts success
    assert response.json == []  #should return initially empty inventory

@patch("inventory.app.test_client") #mocks add function
def test_add_item(mock_client, client):
    print("Test adding an item to the inventory")
    item_data = { #item info
        "name": "Shirt",
        "quantity": 10,
        "price": 200,
        "color": "Green",
    }
    mock_client.return_value.post.return_value = type("Response", (object,), {
        "status_code": 201,
        "json": {"message": "Item added successfully", "item": item_data}
    })
    response = client.post("/add", json=item_data)#sends item
    print("Adding item - Name: Shirt, Quantity: 10, Price: 200, Color: Green")
    
    assert response.status_code == 201 #checks for 201 creatd response

def test_get_inventory(client):
    print("Test retrieving inventory with one item")
    response = client.get("/inventory")
    assert response.status_code == 200
    assert len(response.json) == 1  #inventory should have 1 item

#mocks removing an item 
@patch("inventory.app.test_client")
def test_remove_item(mock_client, client):
    print("Test removing an item from inventory")
    item_id = 0
    mock_client.return_value.delete.return_value = type("Response", (object,), {
        "status_code": 200,
        "json": {"message": f"Item with ID {item_id} removed successfully"}
    })
    response = client.delete("/remove", json={"id": item_id})
    
    assert response.status_code == 200

#mocks attempting to remove an item that doesnt exist
@patch("inventory.app.test_client")
def test_remove_nonexistent_item(mock_client, client):
    print("Test removing an item that does not exist")
    mock_client.return_value.delete.return_value = type("Response", (object,), {
        "status_code": 404,
        "json": {"error": "Item not found"}
    })
    response = client.delete("/remove", json={"id": 999})  # ID that doesn't exist
    
    assert response.status_code == 404

#mocks inventory to ensure item exists
@patch("inventory.inventory", [{"id": 1, "name": "Sweater", "quantity": 53, "price": 500, "color": "Yellow"}])
def test_edit_item(client):
    print("Test editing an item in inventory")

    #ensure item exists before editing
    item_data = {
        "name": "Sweater",
        "quantity": 53,
        "price": 500,
        "color": "Yellow",
    }
    client.post("/add", json=item_data)#add to mock inventory

    #edit  item
    edit_data = {
        "id": 1,  # ID 1
        "name": "Dress",
        "quantity": 8,
        "price": 700,
        "color": "Blue",
    }
    response = client.post("/edit", json=edit_data)

    #make sure ends with edited data
    assert response.status_code == 200
    assert response.json["item"]["name"] == "Dress"
    assert response.json["item"]["quantity"] == 8
    assert response.json["item"]["price"] == 700
    assert response.json["item"]["color"] == "Blue"


#tests editing an item that dont exist
@patch("inventory.app.test_client")
def test_edit_nonexistent_item(mock_client, client):
    print("Test editing an item that does not exist")
    mock_client.return_value.post.return_value = type("Response", (object,), {
        "status_code": 404,
        "json": {"error": "Item not found"}
    })
    response = client.post("/edit", json={"id": 999, "name": "Fake", "quantity": 1, "price": 10, "color": "Red"})
    
    assert response.status_code == 404