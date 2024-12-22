from app import schemas
from .database import client, session
import pytest
from jose import jwt
from app.config import settings


@pytest.fixture
def test_user(client):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "password": "john@123",
    }
    res = client.post("/users/", json=user_data)
    assert  res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_create_user(client):
    res = client.post(
        "/users/",
        json={"name": "John Doe", "email": "johndoe@gmail.com", "password": "john@123"},
    )

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "johndoe@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )

    login_response = schemas.Token(**res.json()) 
    payload = jwt.decode(login_response.access_token, settings.secret_key, settings.algorithm)
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert res.status_code == 200


