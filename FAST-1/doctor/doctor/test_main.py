from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app)

def test_doctors():

    response = client.get("/doctors/")
    assert response.status_code == 200


def test_login():
    response = client.post("/login", json={"username": "chitra@gmail.com", "password": "Chitra#5598"})
    assert response.status_code == 200
    response = client.post("/login", json={"username": "manu@gmail.com", "password": "Manu#5598"})
    assert response.status_code == 404
   
