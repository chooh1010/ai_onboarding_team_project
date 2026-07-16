from math import asin, cos, radians, sin, sqrt

from app.models.tour_content import TourContent
from app.repositories.content_repository import ContentRepository
from app.schemas.content import (
    CategoryCodes,
    ContentDetail,
    ContentListResponse,
    ContentSource,
    ContentSummary,
    ContentTypeItem,
)


def _float_or_zero(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def calculate_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    earth_radius = 6371.0
    d_lat = radians(lat2 - lat1)
    d_lon = radians(lon2 - lon1)
    value = (
        sin(d_lat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(d_lon / 2) ** 2
    )
    return earth_radius * 2 * asin(sqrt(value))


class ContentService:
    def __init__(self, repository: ContentRepository):
        self.repository = repository

    @staticmethod
    def to_summary(
        entity: TourContent,
        distance_km: float | None = None,
    ) -> ContentSummary:
        address = " ".join(part for part in [entity.addr1, entity.addr2] if part).strip()
        return ContentSummary(
            content_id=entity.content_id,
            content_type_id=entity.content_type_id,
            content_type_name=entity.content_type_name,
            title=entity.title,
            address=address,
            latitude=_float_or_zero(entity.mapy),
            longitude=_float_or_zero(entity.mapx),
            thumbnail_url=entity.first_image2 or entity.first_image,
            copyright_code=entity.copyright_code,
            area_code=entity.area_code,
            sigungu_code=entity.sigungu_code,
            event_start_date=entity.event_start_date,
            event_end_date=entity.event_end_date,
            event_place=entity.event_place,
            playtime=entity.playtime,
            use_time_festival=entity.use_time_festival,
            distance_km=round(distance_km, 2) if distance_km is not None else None,
        )

    def list_content_types(self) -> list[ContentTypeItem]:
        return [
            ContentTypeItem(id=content_type_id, name=name, count=count)
            for content_type_id, name, count in self.repository.content_type_counts()
        ]

    def list_contents(self, **kwargs) -> ContentListResponse:
        page = kwargs["page"]
        size = kwargs["size"]
        entities, total = self.repository.search(**kwargs)
        total_pages = (total + size - 1) // size if total else 0
        return ContentListResponse(
            items=[self.to_summary(entity) for entity in entities],
            page=page,
            size=size,
            total_elements=total,
            total_pages=total_pages,
        )

    def get_detail(self, content_id: str) -> ContentDetail | None:
        entity = self.repository.get_by_content_id(content_id)
        if not entity:
            return None
        return ContentDetail(
            content_id=entity.content_id,
            content_type_id=entity.content_type_id,
            content_type_name=entity.content_type_name,
            title=entity.title,
            addr1=entity.addr1,
            addr2=entity.addr2,
            zipcode=entity.zipcode,
            tel=entity.tel,
            longitude=_float_or_zero(entity.mapx),
            latitude=_float_or_zero(entity.mapy),
            first_image=entity.first_image,
            first_image2=entity.first_image2,
            copyright_code=entity.copyright_code,
            area_code=entity.area_code,
            sigungu_code=entity.sigungu_code,
            event_start_date=entity.event_start_date,
            event_end_date=entity.event_end_date,
            event_place=entity.event_place,
            playtime=entity.playtime,
            program=entity.program,
            subevent=entity.subevent,
            sponsor1=entity.sponsor1,
            sponsor1_tel=entity.sponsor1_tel,
            sponsor2=entity.sponsor2,
            sponsor2_tel=entity.sponsor2_tel,
            event_homepage=entity.event_homepage,
            booking_place=entity.booking_place,
            age_limit=entity.age_limit,
            festival_grade=entity.festival_grade,
            place_info=entity.place_info,
            spend_time_festival=entity.spend_time_festival,
            discount_info_festival=entity.discount_info_festival,
            use_time_festival=entity.use_time_festival,
            category_codes=CategoryCodes(
                cat1=entity.cat1,
                cat2=entity.cat2,
                cat3=entity.cat3,
                lcls_system1=entity.lcls_system1,
                lcls_system2=entity.lcls_system2,
                lcls_system3=entity.lcls_system3,
            ),
            source=ContentSource(
                provider="한국관광공사",
                license="공공누리 제3유형",
            ),
        )

    def nearby(
        self,
        *,
        latitude: float,
        longitude: float,
        content_type_id: str | None,
        area_code: str | None,
        radius_km: float,
        limit: int,
    ) -> list[ContentSummary]:
        matches: list[tuple[TourContent, float]] = []
        for entity in self.repository.candidates_for_nearby(
            content_type_id=content_type_id,
            area_code=area_code,
        ):
            distance = calculate_distance_km(
                latitude,
                longitude,
                _float_or_zero(entity.mapy),
                _float_or_zero(entity.mapx),
            )
            if distance <= radius_km:
                matches.append((entity, distance))
        matches.sort(key=lambda item: item[1])
        return [self.to_summary(entity, distance) for entity, distance in matches[:limit]]
