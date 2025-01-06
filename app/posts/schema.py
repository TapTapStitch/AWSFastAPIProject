from fastapi import Query
from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class PostSchema(BaseModel):
    id: UUID
    title: str
    body: str
    tags: List[str]
    createdDate: datetime
    updatedDate: datetime


class CreatePostSchema(BaseModel):
    title: str = Field(..., max_length=200)
    body: str = Field(..., max_length=2000)
    tags: List[str] | None = []


class UpdatePostSchema(BaseModel):
    title: str | None = Field(None, max_length=200)
    body: str | None = Field(None, max_length=2000)
    tags: List[str] | None = None


class Params(BaseModel):
    tags: str | None = Query(None)
    limit: int | None = Query(None)

    def parsed_tags(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(",")]
        return None
