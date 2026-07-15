from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, post_id: int) -> Post | None:
        return self.db.get(Post, post_id)

    def search(
        self,
        *,
        category: str | None,
        keyword: str | None,
        page: int,
        size: int,
    ) -> tuple[list[Post], int]:
        filters = []
        if category:
            filters.append(Post.category == category)
        if keyword:
            pattern = f"%{keyword.strip()}%"
            filters.append(or_(Post.title.ilike(pattern), Post.content.ilike(pattern)))

        total = self.db.scalar(select(func.count(Post.id)).where(*filters)) or 0
        statement = (
            select(Post)
            .where(*filters)
            .order_by(Post.created_at.desc(), Post.id.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        return list(self.db.scalars(statement).all()), total

    def create(self, post: Post) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def save(self, post: Post) -> Post:
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post

    def delete(self, post: Post) -> None:
        self.db.delete(post)
        self.db.commit()
