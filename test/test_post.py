import pytest
from app import schema

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    def validate(post):
        return schema.PostOut(**res.json())
    posts_map = map(validate,res.json())
    posts_list = list(posts_map)
    print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

# def test_posts_empty(authorized_client):
#     res = authorized_client.get("/posts/")
#     print(res.json())
#     assert res.status_code == 401

# def test_create_post(authorized_client):
#     res = authorized_client.post("/posts/", json={"title" : "ffdgfdg","content":"123456"}) 

#     newpost = schema.Post(**res.json())
#     assert newpost.content == "123456"
#     assert res.status_code == 201

def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schema.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schema.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']