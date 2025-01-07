import pytest
from uuid import uuid4


@pytest.fixture
def create_sample_post(client):
    post_data = {
        "title": "Sample Post",
        "body": "This is a sample post for testing purposes.",
        "tags": ["sample", "test"],
    }
    response = client.post("/posts", json=post_data)
    assert response.status_code == 201
    return response.json()


# Test for fetching all posts
def test_get_posts(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test for creating a new post
def test_create_post(client):
    data = {"title": "Test Title", "body": "Test Body", "tags": ["tag1", "tag2"]}
    response = client.post("/posts", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == "Test Title"
    assert response_data["body"] == "Test Body"
    assert response_data["tags"] == ["tag1", "tag2"]
    assert "id" in response_data
    assert "createdDate" in response_data
    assert "updatedDate" in response_data


# Test for fetching a post by ID - successful case
def test_get_existing_post(client, create_sample_post):
    post_id = create_sample_post["id"]
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == post_id
    assert "title" in response_data
    assert "body" in response_data
    assert "tags" in response_data
    assert "createdDate" in response_data
    assert "updatedDate" in response_data


# Test for fetching a post by ID - non-existent case
def test_get_nonexistent_post(client):
    post_id = uuid4()
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for updating a post - successful case
def test_update_existing_post(client, create_sample_post):
    post_id = create_sample_post["id"]
    data = {"title": "Updated Title", "body": "Updated Body", "tags": ["tag3"]}
    response = client.patch(f"/post/{post_id}", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Updated Title"
    assert response_data["body"] == "Updated Body"
    assert response_data["tags"] == ["tag3"]
    assert "id" in response_data
    assert "createdDate" in response_data
    assert "updatedDate" in response_data


# Test for updating a non-existent post
def test_update_nonexistent_post(client):
    post_id = uuid4()
    data = {"title": "Updated Title"}
    response = client.patch(f"/post/{post_id}", json=data)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for deleting a post - successful case
def test_delete_existing_post(client, create_sample_post):
    post_id = create_sample_post["id"]
    response = client.delete(f"/post/{post_id}")
    assert response.status_code == 204
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for deleting a non-existent post
def test_delete_nonexistent_post(client):
    post_id = uuid4()
    response = client.delete(f"/post/{post_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for fetching posts with query parameters
def test_get_posts_with_params(client):
    params = {"tags": "tag1,tag2", "limit": 10}
    response = client.get("/posts", params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)


# Test for creating a post with missing required fields
def test_create_post_missing_fields(client):
    data = {"title": "Test Title"}  # Missing 'body' and 'tags'
    response = client.post("/posts", json=data)
    assert response.status_code == 422
    response_data = response.json()
    assert "detail" in response_data
