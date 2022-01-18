from app.main import app
from fastapi.testclient import TestClient
from pytest import fixture

client = TestClient(app)

@fixture(scope='class')
def setup():
    print("START FIXTURE")
    yield {"data":"123"}
    print("END FIXTURE")

def test_root(setup):
    response = client.get("/")
    print("test_root - ",response.json())
    assert response.json().get('message') == 'Hello World !'

def test_root2(setup):
    response = client.get("/")
    print("test_root2 - ",response.json())
    assert response.json().get('message') == 'Hello World !'