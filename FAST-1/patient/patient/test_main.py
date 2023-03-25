from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app)

def test_patients():
    response = client.get('/patients')
    assert response.status_code == 200
   

def test_login():
    response = client.post("/login", json={"username": "marium@gmail.com", "password": "Marium#5598"})
    assert response.status_code == 200
    response = client.post("/login", json={"username": "manu@gmail.com", "password": "Manu#5598"})
    assert response.status_code == 200

def test_create_patient():
    response = client.post("/patients", json={"name": "Gopinath", "email": "gopinath@gmail.com", "password": "Gopinath#5598", "phone_number": "7867564253"})
    assert response.status_code == 200
    assert response.json()["name"] == "Gopinath"
    assert response.json()["email"] == "gopinath@gmail.com"
    assert "password" not in response.json()  # ensure password is not returned in response
    assert response.json()["phone_number"] == "7867564253"
    # ensure patient was added to database
    response = client.get(f"/patients/{response.json()['pat_id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Gopinath"



def test_delete_patient():
    # create test patients to delete
    response1 = client.post("/patients", json={"name": "Charan", "email": "charan@gmail.com", "password": "Charan#5598", "phone_number": "8867564253"})
    assert response1.status_code == 200
    pat_id1 = response1.json()["pat_id"]
    response2 = client.post("/patients", json={"name": "John", "email": "john@example.com", "password": "John#1234", "phone_number": "555-555-5555"})
    assert response2.status_code == 200
    pat_id2 = response2.json()["pat_id"]
    # delete one of the patients
    response = client.delete(f"/patients/{pat_id2}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # ensure deleted patient was deleted from database
    response = client.get(f"/patients/{pat_id2}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # ensure other patient still exists
    response = client.get(f"/patients/{pat_id1}")
    assert response.status_code == 200
    assert response.json()["name"] == "John"


