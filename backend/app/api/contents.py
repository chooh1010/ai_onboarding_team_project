from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.content_repository import ContentRepository
from app.schemas.content import (
    ContentDetail,
    ContentListResponse,
    ContentSummary,
    ContentTypeListResponse,
)
from app.services.content_service import ContentService

router = APIRouter(prefix="/api", tags=["contents"])


def get_service(db: Session = Depends(get_db)) -> ContentService:
    return ContentService(ContentRepository(db))


@router.get("/content-types", response_model=ContentTypeListResponse)
def list_content_types(service: ContentService = Depends(get_service)):
    return ContentTypeListResponse(items=service.list_content_types())


@router.get("/contents", response_model=ContentListResponse)
def list_contents(
    content_type_id: str | None = Query(default=None, alias="contentTypeId"),
    area_code: str | None = Query(default=None, alias="areaCode"),
    sigungu_code: str | None = Query(default=None, alias="sigunguCode"),
    keyword: str | None = None,
    has_image: bool | None = Query(default=None, alias="hasImage"),
    query_start_date: str | None = Query(
        default=None,
        alias="queryStartDate",
        pattern=r"^\d{8}$",
        description="조회 기간 시작일(YYYYMMDD)",
    ),
    query_end_date: str | None = Query(
        default=None,
        alias="queryEndDate",
        pattern=r"^\d{8}$",
        description="조회 기간 종료일(YYYYMMDD)",
    ),
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query(ge=1, le=100)] = 12,
    sort: Literal["title", "-title", "newest", "type", "event-date"] = "title",
    service: ContentService = Depends(get_service),
):
    return service.list_contents(
        content_type_id=content_type_id,
        area_code=area_code,
        sigungu_code=sigungu_code,
        keyword=keyword,
        has_image=has_image,
        query_start_date=query_start_date,
        query_end_date=query_end_date,
        page=page,
        size=size,
        sort=sort,
    )


@router.get("/contents/nearby", response_model=list[ContentSummary])
def nearby_contents(
    latitude: Annotated[float, Query(ge=-90, le=90)],
    longitude: Annotated[float, Query(ge=-180, le=180)],
    content_type_id: str | None = Query(default=None, alias="contentTypeId"),
    area_code: str | None = Query(default=None, alias="areaCode"),
    radius_km: Annotated[float, Query(alias="radiusKm", gt=0, le=100)] = 5,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    service: ContentService = Depends(get_service),
):
    return service.nearby(
        latitude=latitude,
        longitude=longitude,
        content_type_id=content_type_id,
        area_code=area_code,
        radius_km=radius_km,
        limit=limit,
    )


@router.get("/contents/{content_id}", response_model=ContentDetail)
def get_content(content_id: str, service: ContentService = Depends(get_service)):
    detail = service.get_detail(content_id)
    if not detail:
        raise HTTPException(status_code=404, detail="관광 콘텐츠를 찾을 수 없습니다.")
    return detail
