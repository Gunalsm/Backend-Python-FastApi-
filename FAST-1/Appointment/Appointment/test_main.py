from fastapi.testclient import TestClient
from main import app
from fastapi import status

client = TestClient(app)

def test_appointments():
    response = client.get('/appointments')
    assert response.status_code == 200

def test_get_appointId():
    response = client.get('/appointment/1')
    assert response.status_code == 200

    # response = client.get('/appointment/100')
    # assert response.status_code == 404
