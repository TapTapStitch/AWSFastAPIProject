import pytest
from uuid import uuid4, UUID
from fastapi import HTTPException
from app.posts.schema import CreatePostSchema, UpdatePostSchema, Params


def test_create_post(posts_crud):
    data = CreatePostSchema(title="Test Title", body="Test Body", tags=["tag1", "tag2"])
    result = posts_crud.create_post(data)
    assert result["title"] == "Test Title"
    assert result["body"] == "Test Body"
    assert result["tags"] == ["tag1", "tag2"]
    assert "id" in result
    assert "createdDate" in result
    assert "updatedDate" in result


def test_get_posts(posts_crud):
    data1 = CreatePostSchema(title="Title1", body="Body1", tags=["tag1"])
    data2 = CreatePostSchema(title="Title2", body="Body2", tags=["tag2"])
    posts_crud.create_post(data1)
    posts_crud.create_post(data2)
    params = Params(limit=1, tags="tag1")
    result = posts_crud.get_posts(params)
    assert len(result) == 1
    assert result[0]["title"] == "Title1"

def test_get_public_posts(posts_crud):
    data1 = CreatePostSchema(title="Title1", body="Body1", tags=["tag1"])
    data2 = CreatePostSchema(title="Title2", body="Body2", tags=["tag2"])
    posts_crud.create_post(data1)
    posts_crud.create_post(data2)
    params = Params()
    result = posts_crud.get_posts(params, public=True)
    assert len(result) == 2
    assert not "id" in result[0]
    assert not "id" in result[1]


def test_get_post(posts_crud):
    data = CreatePostSchema(title="Test Title", body="Test Body", tags=["tag1"])
    created_post = posts_crud.create_post(data)
    post_id = UUID(created_post["id"])
    result = posts_crud.get_post(post_id)
    assert result["title"] == "Test Title"


def test_get_post_not_found(posts_crud):
    with pytest.raises(HTTPException) as exc_info:
        posts_crud.get_post(UUID(str(uuid4())))
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_update_post(posts_crud):
    data = CreatePostSchema(title="Original Title", body="Original Body", tags=["tag1"])
    created_post = posts_crud.create_post(data)
    post_id = UUID(created_post["id"])
    update_data = UpdatePostSchema(title="Updated Title")
    result = posts_crud.update_post(post_id, update_data)
    assert result["title"] == "Updated Title"
    assert result["body"] == "Original Body"


def test_update_post_not_found(posts_crud):
    update_data = UpdatePostSchema(title="Updated Title")
    with pytest.raises(HTTPException) as exc_info:
        posts_crud.update_post(UUID(str(uuid4())), update_data)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_delete_post(posts_crud):
    data = CreatePostSchema(title="Test Title", body="Test Body", tags=["tag1"])
    created_post = posts_crud.create_post(data)
    post_id = UUID(created_post["id"])
    posts_crud.delete_post(post_id)
    with pytest.raises(HTTPException) as exc_info:
        posts_crud.get_post(post_id)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"


def test_delete_post_not_found(posts_crud):
    with pytest.raises(HTTPException) as exc_info:
        posts_crud.delete_post(UUID(str(uuid4())))
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Post not found"
