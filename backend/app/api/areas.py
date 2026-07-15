from fastapi import APIRouter

from app.schemas.content import AreaItem, AreaListResponse

router = APIRouter(prefix="/api/areas", tags=["areas"])


@router.get("", response_model=AreaListResponse)
def list_areas() -> AreaListResponse:
    gwangju_children = [
        AreaItem(name="광산구", area_code="5", sigungu_code="1"),
        AreaItem(name="남구", area_code="5", sigungu_code="2"),
        AreaItem(name="동구", area_code="5", sigungu_code="3"),
        AreaItem(name="북구", area_code="5", sigungu_code="4"),
        AreaItem(name="서구", area_code="5", sigungu_code="5"),
    ]
    items = [
        AreaItem(name="광주", area_code="5", children=gwangju_children),
        AreaItem(name="담양", area_code="38", sigungu_code="7"),
        AreaItem(name="나주", area_code="38", sigungu_code="6"),
        AreaItem(name="화순", area_code="38", sigungu_code="24"),
        AreaItem(name="장성", area_code="38", sigungu_code="19"),
        AreaItem(name="여수", area_code="38", sigungu_code="13"),
        AreaItem(name="해남", area_code="38", sigungu_code="23"),
        AreaItem(name="진도", area_code="38", sigungu_code="21"),
        AreaItem(name="순천", area_code="38", sigungu_code="11"),
        AreaItem(name="전주", area_code="37", sigungu_code="12"),
        AreaItem(name="남원", area_code="37", sigungu_code="4"),
    ]
    return AreaListResponse(items=items)
