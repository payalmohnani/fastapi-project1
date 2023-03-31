from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings 
from app.database import get_db
from app import models
from alembic import command
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    # command.upgrade("head")
    # command.downgrade("base")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user1(client):
    user_data = {"email": "random@mail.com", "password": "123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "user2@mail.com", "password": "password123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user1):
    return create_access_token({"current_user": test_user1["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user1, test_user2, session):
    test_post_data = [
    {
        "title" : "first title",
        "content": "first content",
        "owner_id": test_user1["id"]
    },
    {
        "title" : "second title",
        "content": "second content",
        "owner_id": test_user1["id"]
    },
    {
        "title" : "third title",
        "content": "third content",
        "owner_id": test_user1["id"]
    }, 
    {
        "title" : "fourth title",
        "content": "fourth content",
        "owner_id": test_user2["id"]
    } 
    ]
    
    all_posts = [models.Post(**test_post) for test_post in test_post_data]

    session.add_all(all_posts)

    session.commit()
    session.query(models.Post).all()
    return all_posts

