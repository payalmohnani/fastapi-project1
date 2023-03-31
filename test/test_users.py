import pytest
from app import schemas
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    assert(res.json()) == {"message": "Hello World"}
    assert(res.status_code) == 200


def test_create_user(client):
    res = client.post("/users", json={"email": "random@mail.com", "password": "password123"})
    assert res.status_code == 201


def test_login_user(client, test_user1):
    res = client.post("/login", data={"username": test_user1["email"], "password": test_user1["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload["current_user"]
    assert id == test_user1["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code",{
    ("wrongmail@mail.com", "password123", 404),
    ("random@mail.com", "wrong_password", 404),
    (None, "password123", 422),
    ("random@mail.com", None, 422 )   
})
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code