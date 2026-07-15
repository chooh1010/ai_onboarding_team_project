from fastapi import HTTPException, status

from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.schemas.post import (
    PostCreate,
    PostDetail,
    PostListResponse,
    PostSummary,
    PostUpdate,
)


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    @staticmethod
    def to_summary(post: Post) -> PostSummary:
        return PostSummary.model_validate(post)

    @staticmethod
    def to_detail(post: Post) -> PostDetail:
        return PostDetail.model_validate(post)

    def list_posts(
        self,
        *,
        category: str | None,
        keyword: str | None,
        page: int,
        size: int,
    ) -> PostListResponse:
        posts, total = self.repository.search(
            category=category,
            keyword=keyword,
            page=page,
            size=size,
        )
        return PostListResponse(
            items=[self.to_summary(post) for post in posts],
            page=page,
            size=size,
            total_elements=total,
            total_pages=(total + size - 1) // size if total else 0,
        )

    def get_detail(self, post_id: int, increase_view: bool = True) -> PostDetail:
        post = self.repository.get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        if increase_view:
            post.view_count += 1
            post = self.repository.save(post)
        return self.to_detail(post)

    def create(self, payload: PostCreate) -> PostDetail:
        post = Post(
            category=payload.category.value,
            title=payload.title.strip(),
            content=payload.content.strip(),
            edit_password=payload.password,
        )
        return self.to_detail(self.repository.create(post))

    def update(self, post_id: int, payload: PostUpdate) -> PostDetail:
        post = self._get_and_verify(post_id, payload.password)
        post.title = payload.title.strip()
        post.content = payload.content.strip()
        return self.to_detail(self.repository.save(post))

    def delete(self, post_id: int, password: str) -> None:
        post = self._get_and_verify(post_id, password)
        self.repository.delete(post)

    def _get_and_verify(self, post_id: int, password: str) -> Post:
        post = self.repository.get(post_id)
        if not post:
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
        if post.edit_password != password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="비밀번호가 일치하지 않습니다.",
            )
        return post
