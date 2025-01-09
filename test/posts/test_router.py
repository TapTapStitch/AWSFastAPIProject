import pytest
from uuid import uuid4
from app.posts.schema import CreatePostSchema


@pytest.fixture
def create_sample_post(posts_crud):
    data = CreatePostSchema(title="Test Title", body="Test Body", tags=["tag1", "tag2"])
    result = posts_crud.create_post(data)
    return result


# Test for fetching all posts (Unauthorized)
def test_get_posts_unauthorized(client):
    response = client.get("/posts")
    assert response.status_code == 401


# Test for fetching public posts (public endpoint, should not require auth)
def test_get_public_posts_unauthorized(client):
    response = client.get("/public/posts")
    assert response.status_code == 200  # Public endpoint, so no 401 here


# Test for creating a new post (Unauthorized)
def test_create_post_unauthorized(client):
    data = {"title": "Test Title", "body": "Test Body", "tags": ["tag1", "tag2"]}
    response = client.post("/posts", json=data)
    assert response.status_code == 401


# Test for fetching a post by ID (Unauthorized)
def test_get_existing_post_unauthorized(client, create_sample_post):
    post_id = create_sample_post["id"]
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 401


# Test for fetching a non-existent post (Unauthorized)
def test_get_nonexistent_post_unauthorized(client):
    post_id = uuid4()
    response = client.get(f"/post/{post_id}")
    assert response.status_code == 401


# Test for updating a post (Unauthorized)
def test_update_existing_post_unauthorized(client, create_sample_post):
    post_id = create_sample_post["id"]
    data = {"title": "Updated Title", "body": "Updated Body", "tags": ["tag3"]}
    response = client.patch(f"/post/{post_id}", json=data)
    assert response.status_code == 401


# Test for updating a non-existent post (Unauthorized)
def test_update_nonexistent_post_unauthorized(client):
    post_id = uuid4()
    data = {"title": "Updated Title"}
    response = client.patch(f"/post/{post_id}", json=data)
    assert response.status_code == 401


# Test for deleting a post (Unauthorized)
def test_delete_existing_post_unauthorized(client, create_sample_post):
    post_id = create_sample_post["id"]
    response = client.delete(f"/post/{post_id}")
    assert response.status_code == 401


# Test for deleting a non-existent post (Unauthorized)
def test_delete_nonexistent_post_unauthorized(client):
    post_id = uuid4()
    response = client.delete(f"/post/{post_id}")
    assert response.status_code == 401


# Test for fetching posts with query parameters (Unauthorized)
def test_get_posts_with_params_unauthorized(client):
    params = {"tags": "tag1,tag2", "limit": 10}
    response = client.get("/posts", params=params)
    assert response.status_code == 401


# Test for creating a post with missing required fields (Unauthorized)
def test_create_post_missing_fields_unauthorized(client):
    data = {"title": "Test Title"}  # Missing 'body' and 'tags'
    response = client.post("/posts", json=data)
    assert response.status_code == 401


# Test for fetching all posts (Authorized)
def test_get_posts_authenticated(authenticated_client):
    response = authenticated_client.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test for fetching public posts (Public endpoint, should not require auth)
def test_get_public_posts_authenticated(authenticated_client):
    response = authenticated_client.get("/public/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Test for creating a new post (Authorized)
def test_create_post_authenticated(authenticated_client):
    data = {"title": "Test Title", "body": "Test Body", "tags": ["tag1", "tag2"]}
    response = authenticated_client.post("/posts", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == "Test Title"
    assert response_data["body"] == "Test Body"
    assert response_data["tags"] == ["tag1", "tag2"]
    assert "id" in response_data
    assert "createdDate" in response_data
    assert "updatedDate" in response_data


# Test for fetching a post by ID (Authorized)
def test_get_existing_post_authenticated(authenticated_client, create_sample_post):
    post_id = create_sample_post["id"]
    response = authenticated_client.get(f"/post/{post_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == post_id
    assert "title" in response_data
    assert "body" in response_data
    assert "tags" in response_data
    assert "createdDate" in response_data
    assert "updatedDate" in response_data


# Test for fetching a non-existent post (Authorized)
def test_get_nonexistent_post_authenticated(authenticated_client):
    post_id = uuid4()
    response = authenticated_client.get(f"/post/{post_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for updating a post (Authorized)
def test_update_existing_post_authenticated(authenticated_client, create_sample_post):
    post_id = create_sample_post["id"]
    data = {"title": "Updated Title", "body": "Updated Body", "tags": ["tag3"]}
    response = authenticated_client.patch(f"/post/{post_id}", json=data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == "Updated Title"
    assert response_data["body"] == "Updated Body"
    assert response_data["tags"] == ["tag3"]
    assert "id" in response_data
    assert "createdDate" in response_data
    assert "updatedDate" in response_data


# Test for updating a non-existent post (Authorized)
def test_update_nonexistent_post_authenticated(authenticated_client):
    post_id = uuid4()
    data = {"title": "Updated Title"}
    response = authenticated_client.patch(f"/post/{post_id}", json=data)
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for deleting a post (Authorized)
def test_delete_existing_post_authenticated(authenticated_client, create_sample_post):
    post_id = create_sample_post["id"]
    response = authenticated_client.delete(f"/post/{post_id}")
    assert response.status_code == 204
    response = authenticated_client.get(f"/post/{post_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for deleting a non-existent post (Authorized)
def test_delete_nonexistent_post_authenticated(authenticated_client):
    post_id = uuid4()
    response = authenticated_client.delete(f"/post/{post_id}")
    assert response.status_code == 404
    response_data = response.json()
    assert response_data == {"detail": "Post not found"}


# Test for fetching posts with query parameters (Authorized)
def test_get_posts_with_params_authenticated(authenticated_client):
    params = {"tags": "tag1,tag2", "limit": 10}
    response = authenticated_client.get("/posts", params=params)
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)


# Test for creating a post with missing required fields (Authorized)
def test_create_post_missing_fields_authenticated(authenticated_client):
    data = {"title": "Test Title"}  # Missing 'body' and 'tags'
    response = authenticated_client.post("/posts", json=data)
    assert response.status_code == 422
    response_data = response.json()
    assert "detail" in response_data
