from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.data_source import DataSource

router = APIRouter(prefix="/api/data-source", tags=["data-source"])


@router.get("")
def get_data_source(db: Session = Depends(get_db)):
    source = db.scalar(select(DataSource).limit(1))
    if not source:
        return {
            "provider": "한국관광공사",
            "datasetName": "국문 관광정보 서비스",
            "apiName": "TourAPI 4.0",
            "region": "광주_전라권",
            "licenseName": "공공누리 제3유형",
            "commercialUse": True,
            "modificationAllowed": False,
            "sourceUrl": "https://www.data.go.kr/data/15101578/openapi.do",
            "collectedAt": None,
            "collectedAtNote": "제공 기관 또는 데이터 제공 담당자 확인 필요",
            "attributionText": "이 서비스는 한국관광공사 TourAPI 4.0 데이터를 활용하였습니다.",
        }
    return {
        "provider": source.provider,
        "datasetName": source.dataset_name,
        "apiName": source.api_name,
        "region": source.region,
        "licenseName": source.license_name,
        "commercialUse": source.commercial_use,
        "modificationAllowed": source.modification_allowed,
        "sourceUrl": source.source_url,
        "collectedAt": source.collected_at,
        "collectedAtNote": (
            None
            if source.collected_at
            else "제공 기관 또는 데이터 제공 담당자 확인 필요"
        ),
        "attributionText": source.attribution_text,
    }
