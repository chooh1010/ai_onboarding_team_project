from warnings import filters

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.tour_content import TourContent


class ContentRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_all(self) -> int:
        return self.db.scalar(select(func.count(TourContent.id))) or 0

    def get_by_content_id(self, content_id: str) -> TourContent | None:
        return self.db.scalar(
            select(TourContent).where(TourContent.content_id == content_id)
        )

    def content_type_counts(self) -> list[tuple[str, str, int]]:
        statement = (
            select(
                TourContent.content_type_id,
                TourContent.content_type_name,
                func.count(TourContent.id),
            )
            .group_by(TourContent.content_type_id, TourContent.content_type_name)
            .order_by(TourContent.content_type_id)
        )
        return list(self.db.execute(statement).all())

    def search(
        self,
        *,
        content_type_id: str | None = None,
        area_code: str | None = None,
        sigungu_code: str | None = None,
        keyword: str | None = None,
        has_image: bool | None = None,
        page: int = 1,
        size: int = 12,
        sort: str = "title",
    ) -> tuple[list[TourContent], int]:
        filters = []
        if content_type_id:
            filters.append(TourContent.content_type_id == content_type_id)
        if area_code:
            filters.append(TourContent.area_code == area_code)
        if sigungu_code:
            filters.append(TourContent.sigungu_code == sigungu_code)
        if keyword:
            pattern = f"%{keyword.strip()}%"
            filters.append(
                or_(
                    TourContent.title.ilike(pattern),
                    TourContent.addr1.ilike(pattern),
                    TourContent.addr2.ilike(pattern),
                )
            )
        if has_image is True:
            filters.append(TourContent.first_image != "")

        count_statement = select(func.count(TourContent.id)).where(*filters)
        total = self.db.scalar(count_statement) or 0

        order_by = {
            "title": TourContent.title.asc(),
            "-title": TourContent.title.desc(),
            "newest": TourContent.source_modified_time.desc(),
            "type": TourContent.content_type_id.asc(),
        }.get(sort, TourContent.title.asc())

        statement = (
            select(TourContent)
            .where(*filters)
            .order_by(order_by, TourContent.id.asc())
            .offset((page - 1) * size)
            .limit(size)
        )
        return list(self.db.scalars(statement).all()), total

    def candidates_for_nearby(
        self,
        *,
        content_type_id: str | None = None,
        area_code: str | None = None,
    ) -> list[TourContent]:
        filters = [TourContent.mapx != "", TourContent.mapy != ""]
        if content_type_id:
            filters.append(TourContent.content_type_id == content_type_id)
        if area_code:
            filters.append(TourContent.area_code == area_code)
        return list(self.db.scalars(select(TourContent).where(*filters)).all())
