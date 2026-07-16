from pydantic import Field

from app.schemas.common import CamelModel


class ContentTypeItem(CamelModel):
    id: str
    name: str
    count: int


class ContentTypeListResponse(CamelModel):
    items: list[ContentTypeItem]


class AreaItem(CamelModel):
    name: str
    area_code: str
    sigungu_code: str | None = None
    children: list["AreaItem"] = Field(default_factory=list)


class AreaListResponse(CamelModel):
    items: list[AreaItem]


class ContentSummary(CamelModel):
    content_id: str
    content_type_id: str
    content_type_name: str
    title: str
    address: str
    latitude: float
    longitude: float
    thumbnail_url: str
    copyright_code: str
    area_code: str
    sigungu_code: str
    event_start_date: str = ""
    event_end_date: str = ""
    event_place: str = ""
    playtime: str = ""
    use_time_festival: str = ""
    distance_km: float | None = None


class ContentListResponse(CamelModel):
    items: list[ContentSummary]
    page: int
    size: int
    total_elements: int
    total_pages: int


class CategoryCodes(CamelModel):
    cat1: str
    cat2: str
    cat3: str
    lcls_system1: str
    lcls_system2: str
    lcls_system3: str


class ContentSource(CamelModel):
    provider: str
    license: str


class ContentDetail(CamelModel):
    content_id: str
    content_type_id: str
    content_type_name: str
    title: str
    addr1: str
    addr2: str
    zipcode: str
    tel: str
    longitude: float
    latitude: float
    first_image: str
    first_image2: str
    copyright_code: str
    area_code: str
    sigungu_code: str
    event_start_date: str = ""
    event_end_date: str = ""
    event_place: str = ""
    playtime: str = ""
    program: str = ""
    subevent: str = ""
    sponsor1: str = ""
    sponsor1_tel: str = ""
    sponsor2: str = ""
    sponsor2_tel: str = ""
    event_homepage: str = ""
    booking_place: str = ""
    age_limit: str = ""
    festival_grade: str = ""
    place_info: str = ""
    spend_time_festival: str = ""
    discount_info_festival: str = ""
    use_time_festival: str = ""
    category_codes: CategoryCodes
    source: ContentSource
