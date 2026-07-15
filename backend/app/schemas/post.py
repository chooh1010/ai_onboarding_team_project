from datetime import datetime
from enum import StrEnum

from pydantic import Field

from app.schemas.common import CamelModel


class PostCategory(StrEnum):
    TOURISM = "TOURISM"
    FOOD = "FOOD"
    LODGING = "LODGING"
    FESTIVAL = "FESTIVAL"
    COURSE = "COURSE"
    FREE = "FREE"


class PostCreate(CamelModel):
    category: PostCategory
    title: str = Field(min_length=2, max_length=100)
    content: str = Field(min_length=1, max_length=5000)
    password: str = Field(min_length=4, max_length=30)


class PostUpdate(CamelModel):
    title: str = Field(min_length=2, max_length=100)
    content: str = Field(min_length=1, max_length=5000)
    password: str = Field(min_length=4, max_length=30)


class PasswordRequest(CamelModel):
    password: str = Field(min_length=4, max_length=30)


class PostSummary(CamelModel):
    id: int
    category: PostCategory
    title: str
    view_count: int
    created_at: datetime
    updated_at: datetime


class PostDetail(PostSummary):
    content: str


class PostListResponse(CamelModel):
    items: list[PostSummary]
    page: int
    size: int
    total_elements: int
    total_pages: int
