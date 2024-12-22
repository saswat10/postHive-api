from app import schemas
from jose import jwt
from app.config import settings
import pytest


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

@pytest.mark.parametrize("email, password, status_code", [
    ("wrong@email.com", "john@123", 403),
    ("johndoe@gmail.com", "wrong@123", 403),
    ("wrong@email.com", "wrong@123", 403),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login/", data={"username": email, "password": password}
    )
    
    print(res.json())
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"