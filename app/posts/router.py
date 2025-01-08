from fastapi import APIRouter, Depends, Response
from uuid import UUID
from typing import List
from app.posts.schema import (
    PostSchema,
    PublicPostSchema,
    CreatePostSchema,
    UpdatePostSchema,
    Params,
)
from app.posts.crud import PostsCrud
from app.auth.service import AuthService
from app.posts.swagger_responces import (
    unauthorized_response,
    not_found_response,
    bad_request_response,
)

router = APIRouter()


def get_posts_crud():
    return PostsCrud()


@router.get("/posts", response_model=List[PostSchema], responses=unauthorized_response)
async def get_posts(
    params: Params = Depends(),
    posts_crud: PostsCrud = Depends(get_posts_crud),
    authenticated: dict = Depends(AuthService().authenticate_user),
):
    return posts_crud.get_posts(params)


@router.get("/public/posts", response_model=List[PublicPostSchema])
async def get_posts(
    params: Params = Depends(), posts_crud: PostsCrud = Depends(get_posts_crud)
):
    return posts_crud.get_posts(params, public=True)


@router.post(
    "/posts",
    response_model=PostSchema,
    status_code=201,
    responses=unauthorized_response,
)
async def create_post(
    post: CreatePostSchema,
    posts_crud: PostsCrud = Depends(get_posts_crud),
    authenticated: dict = Depends(AuthService().authenticate_user),
):
    return posts_crud.create_post(post)


@router.get(
    "/post/{id}",
    response_model=PostSchema,
    responses={**unauthorized_response, **not_found_response},
)
async def get_post(
    id: UUID,
    posts_crud: PostsCrud = Depends(get_posts_crud),
    authenticated: dict = Depends(AuthService().authenticate_user),
):
    return posts_crud.get_post(id)


@router.patch(
    "/post/{id}",
    response_model=PostSchema,
    responses={
        **unauthorized_response,
        **not_found_response,
        **bad_request_response,
    },
)
async def update_post(
    id: UUID,
    post: UpdatePostSchema,
    posts_crud: PostsCrud = Depends(get_posts_crud),
    authenticated: dict = Depends(AuthService().authenticate_user),
):
    return posts_crud.update_post(id, post)


@router.delete(
    "/post/{id}",
    status_code=204,
    responses={**unauthorized_response, **not_found_response},
)
async def delete_post(
    id: UUID,
    posts_crud: PostsCrud = Depends(get_posts_crud),
    authenticated: dict = Depends(AuthService().authenticate_user),
):
    posts_crud.delete_post(id)
    return Response(status_code=204)
