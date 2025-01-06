from fastapi import APIRouter, Depends, Response
from uuid import UUID
from typing import List
from app.posts.schema import PostSchema, CreatePostSchema, UpdatePostSchema, Params
from app.posts.crud import PostsCrud

router = APIRouter()


def get_posts_crud():
    return PostsCrud()


@router.get("/posts", response_model=List[PostSchema])
async def get_posts(
    params: Params = Depends(), posts_crud: PostsCrud = Depends(get_posts_crud)
):
    return posts_crud.get_posts(params)


@router.post("/posts", response_model=PostSchema, status_code=201)
async def create_post(
    post: CreatePostSchema, posts_crud: PostsCrud = Depends(get_posts_crud)
):
    return posts_crud.create_post(post)


@router.get(
    "/post/{id}",
    response_model=PostSchema,
    responses={
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "post_not_found": {
                            "summary": "Post not found",
                            "value": {"detail": "Post not found"},
                        }
                    }
                }
            },
        }
    },
)
async def get_post(id: UUID, posts_crud: PostsCrud = Depends(get_posts_crud)):
    return posts_crud.get_post(id)


@router.patch(
    "/post/{id}",
    response_model=PostSchema,
    responses={
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "post_not_found": {
                            "summary": "Post not found",
                            "value": {"detail": "Post not found"},
                        }
                    }
                }
            },
        },
        "400": {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "no_data_provided": {
                            "summary": "No data provided for update",
                            "value": {"detail": "No data provided for update"},
                        }
                    }
                }
            },
        },
    },
)
async def update_post(
    id: UUID, post: UpdatePostSchema, posts_crud: PostsCrud = Depends(get_posts_crud)
):
    return posts_crud.update_post(id, post)


@router.delete(
    "/post/{id}",
    status_code=204,
    responses={
        "404": {
            "description": "Not Found",
            "content": {
                "application/json": {
                    "examples": {
                        "post_not_found": {
                            "summary": "Post not found",
                            "value": {"detail": "Post not found"},
                        }
                    }
                }
            },
        }
    },
)
async def delete_post(id: UUID, posts_crud: PostsCrud = Depends(get_posts_crud)):
    posts_crud.delete_post(id)
    return Response(status_code=204)
