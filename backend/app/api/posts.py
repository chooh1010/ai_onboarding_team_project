from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.post_repository import PostRepository
from app.schemas.post import (
    PasswordRequest,
    PostCategory,
    PostCreate,
    PostDetail,
    PostListResponse,
    PostUpdate,
)
from app.services.post_service import PostService

router = APIRouter(prefix="/api/posts", tags=["posts"])


def get_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(PostRepository(db))


@router.get("", response_model=PostListResponse)
def list_posts(
    category: PostCategory | None = None,
    keyword: str | None = None,
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 10,
    service: PostService = Depends(get_service),
):
    return service.list_posts(
        category=category.value if category else None,
        keyword=keyword,
        page=page,
        size=size,
    )


@router.get("/{post_id}", response_model=PostDetail)
def get_post(post_id: int, service: PostService = Depends(get_service)):
    return service.get_detail(post_id)


@router.post("", response_model=PostDetail, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, service: PostService = Depends(get_service)):
    return service.create(payload)


@router.put("/{post_id}", response_model=PostDetail)
def update_post(
    post_id: int,
    payload: PostUpdate,
    service: PostService = Depends(get_service),
):
    return service.update(post_id, payload)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    payload: PasswordRequest,
    service: PostService = Depends(get_service),
):
    service.delete(post_id, payload.password)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
