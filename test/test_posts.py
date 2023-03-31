import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    post_list = [schemas.PostOut(**post) for post in res.json()]

    assert(len(res.json())) == len(test_posts)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")

    assert res.status_code == 401


def test_get_non_existing_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{111111101}")
    
    assert res.status_code == 404


def test_get_post_by_id(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert post.Post.id == test_posts[0].id
    assert res.status_code == 200


def test_unauthorized_user_get_post_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


@pytest.mark.parametrize("title, content, published",[
    ("title 1", "content 1", True),
    ("title 2", "content 2", False),
    ("title 3", "content 3", True)
])
def test_create_post(authorized_client, test_user1, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content 
    assert created_post.published == published
    assert created_post.owner_id == test_user1["id"]


def test_create_post_default(authorized_client, test_user1, test_posts):
    post_data = {"title": "Test title", "content": "Test content"}
    res = authorized_client.post("/posts/", json=post_data)

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == post_data["title"]
    assert created_post.content == post_data["content"]
    assert created_post.published == True
    assert created_post.owner_id == test_user1["id"]


def test_unauthorized_user_create_post(client, test_user1, test_posts):
    post_data = {"title": "Test title", "content": "Test content", "published": False}
    res = client.post("/posts/", json=post_data)

    assert res.status_code == 401


def test_delete_post(authorized_client, test_user1, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204 


def test_unauthorized_user_delete_post(client, test_user1, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_delete_non_existing_post(authorized_client, test_user1, test_posts):
    res = authorized_client.delete(f"/posts/111010011")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user1, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")

    assert res.status_code == 403


def test_update_post(authorized_client, test_user1, test_posts):
    post_data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=post_data)
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 202
    assert updated_post.title == post_data["title"]
    assert updated_post.content == post_data["content"]

def test_update_other_user_post(authorized_client, test_user1, test_posts):
    post_data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=post_data)
    assert res.status_code == 403
    

def test_update_post_non_exist(authorized_client, test_user1, test_posts):
    post_data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }

    res = authorized_client.put("/posts/10000010", json=post_data)
    assert res.status_code == 404


