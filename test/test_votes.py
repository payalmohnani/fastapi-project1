import pytest
from app import models


@pytest.fixture
def test_make_vote(authorized_client, test_posts, session, test_user1):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user1["id"])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201

def test_vote_twice_post(authorized_client, test_posts, test_make_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})

    assert res.status_code == 409


def test_delete_vote_on_post(authorized_client, test_posts, test_make_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    
    assert res.status_code == 201


def test_delete_non_exit_vote(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    
    assert res.status_code == 404

def test_vote_non_exist_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 10001010, "dir": 1})

    assert res.status_code == 404

def test_vote_unauthorized_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    
    assert res.status_code == 401

    