import argparse
import json
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine
from app.models.tour_content import TourContent

EXPECTED_COUNTS = {
    "12": 505,
    "14": 86,
    "15": 17,
    "25": 55,
    "28": 85,
    "32": 191,
    "38": 38,
    "39": 416,
}


def value(item: dict, key: str) -> str:
    raw = item.get(key, "")
    return "" if raw is None else str(raw)


def load_json_file(db: Session, file_path: Path) -> int:
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    items = data.get("items", [])
    declared_total = int(data.get("total", len(items)))
    if declared_total != len(items):
        raise ValueError(
            f"{file_path.name}: total({declared_total})과 items 길이({len(items)})가 다릅니다."
        )

    content_type_name = str(data.get("contentType", ""))
    region = str(data.get("region", "광주_전라권"))
    existing = set(
        db.scalars(
            select(TourContent.content_id).where(
                TourContent.content_id.in_([value(item, "contentid") for item in items])
            )
        ).all()
    )

    entities = []
    for item in items:
        content_id = value(item, "contentid")
        if not content_id or content_id in existing:
            continue
        entities.append(
            TourContent(
                content_id=content_id,
                content_type_id=value(item, "contenttypeid") or str(data.get("contentTypeId", "")),
                content_type_name=content_type_name,
                region_group=region,
                source_file=file_path.name,
                title=value(item, "title"),
                addr1=value(item, "addr1"),
                addr2=value(item, "addr2"),
                zipcode=value(item, "zipcode"),
                tel=value(item, "tel"),
                mapx=value(item, "mapx"),
                mapy=value(item, "mapy"),
                mlevel=value(item, "mlevel"),
                area_code=value(item, "areacode"),
                sigungu_code=value(item, "sigungucode"),
                ldong_regn_cd=value(item, "lDongRegnCd"),
                ldong_signgu_cd=value(item, "lDongSignguCd"),
                cat1=value(item, "cat1"),
                cat2=value(item, "cat2"),
                cat3=value(item, "cat3"),
                lcls_system1=value(item, "lclsSystm1"),
                lcls_system2=value(item, "lclsSystm2"),
                lcls_system3=value(item, "lclsSystm3"),
                first_image=value(item, "firstimage"),
                first_image2=value(item, "firstimage2"),
                copyright_code=value(item, "cpyrhtDivCd"),
                source_created_time=value(item, "createdtime"),
                source_modified_time=value(item, "modifiedtime"),
                raw_json=json.dumps(item, ensure_ascii=False),
            )
        )
    db.add_all(entities)
    db.commit()
    return len(entities)


def seed_all_json_files(db: Session, data_directory: Path) -> int:
    files = sorted(data_directory.glob("광주_전라권_*.json"))
    if not files:
        raise FileNotFoundError(
            f"{data_directory.resolve()}에 광주_전라권_*.json 파일이 없습니다."
        )
    return sum(load_json_file(db, file_path) for file_path in files)


def validate_database(db: Session) -> None:
    total = db.scalar(select(func.count(TourContent.id))) or 0
    duplicate_count = db.scalar(
        select(func.count()).select_from(
            select(TourContent.content_id)
            .group_by(TourContent.content_id)
            .having(func.count(TourContent.id) > 1)
            .subquery()
        )
    ) or 0
    coordinate_missing = db.scalar(
        select(func.count(TourContent.id)).where(
            (TourContent.mapx == "") | (TourContent.mapy == "")
        )
    ) or 0
    rows = db.execute(
        select(TourContent.content_type_id, func.count(TourContent.id))
        .group_by(TourContent.content_type_id)
    ).all()
    counts = {content_type_id: count for content_type_id, count in rows}

    print(f"총 데이터: {total}")
    print(f"contentId 중복 그룹: {duplicate_count}")
    print(f"좌표 누락: {coordinate_missing}")
    print(f"유형별 건수: {counts}")

    if total == 1393 and counts != EXPECTED_COUNTS:
        raise RuntimeError(f"유형별 건수가 명세와 다릅니다: {counts}")
    if duplicate_count:
        raise RuntimeError("contentId 중복이 발견되었습니다.")
    if coordinate_missing:
        raise RuntimeError("좌표 누락이 발견되었습니다.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=None)
    parser.add_argument("--if-empty", action="store_true")
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    settings = get_settings()
    data_directory = args.data_dir or settings.data_directory

    with SessionLocal() as db:
        current = db.scalar(select(func.count(TourContent.id))) or 0
        if args.if_empty and current > 0:
            print(f"기존 데이터 {current}건이 있어 적재를 건너뜁니다.")
            validate_database(db)
            return
        inserted = seed_all_json_files(db, data_directory)
        print(f"신규 적재: {inserted}건")
        validate_database(db)


if __name__ == "__main__":
    main()
