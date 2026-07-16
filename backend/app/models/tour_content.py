from datetime import datetime, timezone

from sqlalchemy import DateTime, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class TourContent(Base):
    __tablename__ = "tour_contents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content_id: Mapped[str] = mapped_column(
        String(30), unique=True, index=True, nullable=False
    )
    content_type_id: Mapped[str] = mapped_column(String(10), index=True, nullable=False)
    content_type_name: Mapped[str] = mapped_column(
        String(30), index=True, nullable=False
    )
    region_group: Mapped[str] = mapped_column(
        String(50), default="광주_전라권", nullable=False
    )
    source_file: Mapped[str] = mapped_column(String(150), nullable=False)
    title: Mapped[str] = mapped_column(String(300), index=True, nullable=False)
    addr1: Mapped[str] = mapped_column(Text, default="", nullable=False)
    addr2: Mapped[str] = mapped_column(Text, default="", nullable=False)
    zipcode: Mapped[str] = mapped_column(String(20), default="", nullable=False)
    tel: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    mapx: Mapped[str] = mapped_column(String(50), default="", nullable=False)
    mapy: Mapped[str] = mapped_column(String(50), default="", nullable=False)
    mlevel: Mapped[str] = mapped_column(String(10), default="", nullable=False)
    area_code: Mapped[str] = mapped_column(
        String(10), index=True, default="", nullable=False
    )
    sigungu_code: Mapped[str] = mapped_column(
        String(10), index=True, default="", nullable=False
    )
    ldong_regn_cd: Mapped[str] = mapped_column(String(20), default="", nullable=False)
    ldong_signgu_cd: Mapped[str] = mapped_column(String(20), default="", nullable=False)
    cat1: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    cat2: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    cat3: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    lcls_system1: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    lcls_system2: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    lcls_system3: Mapped[str] = mapped_column(String(30), default="", nullable=False)
    first_image: Mapped[str] = mapped_column(Text, default="", nullable=False)
    first_image2: Mapped[str] = mapped_column(Text, default="", nullable=False)
    copyright_code: Mapped[str] = mapped_column(String(20), default="", nullable=False)
    source_created_time: Mapped[str] = mapped_column(String(20), default="", nullable=False)
    source_modified_time: Mapped[str] = mapped_column(String(20), default="", nullable=False)

    # 축제공연행사(contentTypeId=15) 전용 상세 일정 필드.
    # 다른 콘텐츠 유형에서는 빈 문자열로 저장한다.
    event_start_date: Mapped[str] = mapped_column(
        String(8), index=True, default="", nullable=False
    )
    event_end_date: Mapped[str] = mapped_column(
        String(8), index=True, default="", nullable=False
    )
    event_place: Mapped[str] = mapped_column(Text, default="", nullable=False)
    playtime: Mapped[str] = mapped_column(Text, default="", nullable=False)
    program: Mapped[str] = mapped_column(Text, default="", nullable=False)
    subevent: Mapped[str] = mapped_column(Text, default="", nullable=False)
    sponsor1: Mapped[str] = mapped_column(Text, default="", nullable=False)
    sponsor1_tel: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    sponsor2: Mapped[str] = mapped_column(Text, default="", nullable=False)
    sponsor2_tel: Mapped[str] = mapped_column(String(100), default="", nullable=False)
    event_homepage: Mapped[str] = mapped_column(Text, default="", nullable=False)
    booking_place: Mapped[str] = mapped_column(Text, default="", nullable=False)
    age_limit: Mapped[str] = mapped_column(Text, default="", nullable=False)
    festival_grade: Mapped[str] = mapped_column(Text, default="", nullable=False)
    place_info: Mapped[str] = mapped_column(Text, default="", nullable=False)
    spend_time_festival: Mapped[str] = mapped_column(Text, default="", nullable=False)
    discount_info_festival: Mapped[str] = mapped_column(Text, default="", nullable=False)
    use_time_festival: Mapped[str] = mapped_column(Text, default="", nullable=False)

    raw_json: Mapped[str] = mapped_column(Text, nullable=False)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now, nullable=False
    )


Index(
    "idx_tour_content_type_area",
    TourContent.content_type_id,
    TourContent.area_code,
    TourContent.sigungu_code,
)
Index(
    "idx_tour_content_event_period",
    TourContent.content_type_id,
    TourContent.event_start_date,
    TourContent.event_end_date,
)
