from fastapi import APIRouter
from uuid import UUID
from typing import List
from .schema import PostSchema, CreatePostSchema, UpdatePostSchema

router = APIRouter()


@router.get("/posts", response_model=List[PostSchema])
async def get_posts():
    pass


@router.post("/posts", response_model=PostSchema)
async def create_post(post: CreatePostSchema):
    pass


@router.get("/post/{id}", response_model=PostSchema)
async def get_post(id: UUID):
    pass


@router.patch("/post/{id}", response_model=PostSchema)
async def update_post(id: UUID, post: UpdatePostSchema):
    pass


@router.delete("/post/{id}", response_model=PostSchema)
async def delete_post(id: UUID):
    pass
