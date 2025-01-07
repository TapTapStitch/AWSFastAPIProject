import pytest
from uuid import uuid4
from datetime import datetime, timezone
from pydantic import ValidationError
from app.posts.schema import PostSchema, CreatePostSchema, UpdatePostSchema, Params


def test_post_schema_initialization():
    post_data = {
        "id": uuid4(),
        "title": "Sample Post",
        "body": "This is a test body.",
        "tags": ["tag1", "tag2"],
        "createdDate": datetime.now(timezone.utc),
        "updatedDate": datetime.now(timezone.utc),
    }
    post = PostSchema(**post_data)
    assert post.id == post_data["id"]
    assert post.title == post_data["title"]
    assert post.tags == post_data["tags"]


def test_create_post_schema_valid_data():
    data = {
        "title": "Valid Title",
        "body": "Valid body for the post.",
        "tags": ["tag1", "tag2"],
    }
    create_post = CreatePostSchema(**data)
    assert create_post.title == data["title"]
    assert create_post.tags == data["tags"]


def test_create_post_schema_extra_fields():
    data = {
        "title": "Valid Title",
        "body": "Valid body.",
        "tags": ["tag1"],
        "extra_field": "should not be allowed",
    }
    with pytest.raises(ValidationError):
        CreatePostSchema(**data)


def test_create_post_schema_field_constraints():
    with pytest.raises(ValidationError):
        CreatePostSchema(
            title="x" * 201,  # Exceeds max_length
            body="Valid body.",
            tags=["tag1"],
        )


def test_update_post_schema_valid_partial_data():
    data = {"title": "Updated Title"}
    update_post = UpdatePostSchema(**data)
    assert update_post.title == data["title"]
    assert update_post.body is None


def test_update_post_schema_extra_fields():
    data = {"title": "Valid Title", "extra_field": "not allowed"}
    with pytest.raises(ValidationError):
        UpdatePostSchema(**data)


def test_params_schema_valid_data():
    params = Params(tags="tag1,tag2", limit=10)
    assert params.tags == "tag1,tag2"
    assert params.limit == 10
    assert params.parsed_tags() == ["tag1", "tag2"]


def test_params_schema_parsed_tags_none():
    params = Params()
    assert params.parsed_tags() is None


def test_params_schema_extra_fields():
    data = {"tags": "tag1,tag2", "extra_field": "not allowed"}
    with pytest.raises(ValidationError):
        Params(**data)


def test_params_schema_with_invalid_query_data():
    with pytest.raises(ValidationError):
        Params(tags="tag1,tag2", limit="invalid")
