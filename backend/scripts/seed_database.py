import argparse
import json
from pathlib import Path

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import (
    Base,
    SessionLocal,
    engine,
    ensure_tour_content_event_columns,
)
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


FIELD_MAP = {
    "content_type_id": "contenttypeid",
    "title": "title",
    "addr1": "addr1",
    "addr2": "addr2",
    "zipcode": "zipcode",
    "tel": "tel",
    "mapx": "mapx",
    "mapy": "mapy",
    "mlevel": "mlevel",
    "area_code": "areacode",
    "sigungu_code": "sigungucode",
    "ldong_regn_cd": "lDongRegnCd",
    "ldong_signgu_cd": "lDongSignguCd",
    "cat1": "cat1",
    "cat2": "cat2",
    "cat3": "cat3",
    "lcls_system1": "lclsSystm1",
    "lcls_system2": "lclsSystm2",
    "lcls_system3": "lclsSystm3",
    "first_image": "firstimage",
    "first_image2": "firstimage2",
    "copyright_code": "cpyrhtDivCd",
    "source_created_time": "createdtime",
    "source_modified_time": "modifiedtime",
    "event_start_date": "eventstartdate",
    "event_end_date": "eventenddate",
    "event_place": "eventplace",
    "playtime": "playtime",
    "program": "program",
    "subevent": "subevent",
    "sponsor1": "sponsor1",
    "sponsor1_tel": "sponsor1tel",
    "sponsor2": "sponsor2",
    "sponsor2_tel": "sponsor2tel",
    "event_homepage": "eventhomepage",
    "booking_place": "bookingplace",
    "age_limit": "agelimit",
    "festival_grade": "festivalgrade",
    "place_info": "placeinfo",
    "spend_time_festival": "spendtimefestival",
    "discount_info_festival": "discountinfofestival",
    "use_time_festival": "usetimefestival",
}


def value(item: dict, key: str) -> str:
    raw = item.get(key, "")
    return "" if raw is None else str(raw)


def load_json_file(db: Session, file_path: Path) -> tuple[int, int]:
    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    items = data.get("items", [])
    declared_total = int(data.get("total", len(items)))
    if declared_total != len(items):
        raise ValueError(
            f"{file_path.name}: total({declared_total})과 items 길이({len(items)})가 다릅니다."
        )

    content_type_name = str(data.get("contentType", ""))
    content_type_id = str(data.get("contentTypeId", ""))
    region = str(data.get("region", "광주_전라권"))
    content_ids = [value(item, "contentid") for item in items if value(item, "contentid")]
    existing = {
        entity.content_id: entity
        for entity in db.scalars(
            select(TourContent).where(TourContent.content_id.in_(content_ids))
        ).all()
    }

    inserted = 0
    updated = 0
    for item in items:
        content_id = value(item, "contentid")
        if not content_id:
            continue

        entity = existing.get(content_id)
        if entity is None:
            entity = TourContent(
                content_id=content_id,
                content_type_id=value(item, "contenttypeid") or content_type_id,
                content_type_name=content_type_name,
                region_group=region,
                source_file=file_path.name,
                title=value(item, "title"),
                raw_json=json.dumps(item, ensure_ascii=False),
            )
            db.add(entity)
            existing[content_id] = entity
            inserted += 1
        else:
            updated += 1

        entity.content_type_name = content_type_name
        entity.region_group = region
        entity.source_file = file_path.name
        for model_field, json_field in FIELD_MAP.items():
            field_value = value(item, json_field)
            if model_field == "content_type_id" and not field_value:
                field_value = content_type_id
            setattr(entity, model_field, field_value)
        entity.raw_json = json.dumps(item, ensure_ascii=False)

    db.commit()
    return inserted, updated


def seed_all_json_files(db: Session, data_directory: Path) -> tuple[int, int]:
    files = sorted(
        file_path
        for file_path in data_directory.glob("*.json")
        if file_path.is_file()
    )

    if not files:
        raise FileNotFoundError(
            f"{data_directory.resolve()}에 JSON 파일이 없습니다."
        )

    inserted = 0
    updated = 0
    for file_path in files:
        file_inserted, file_updated = load_json_file(db, file_path)
        inserted += file_inserted
        updated += file_updated
    return inserted, updated


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
    festival_date_missing = db.scalar(
        select(func.count(TourContent.id)).where(
            TourContent.content_type_id == "15",
            (TourContent.event_start_date == "") | (TourContent.event_end_date == ""),
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
    print(f"축제 시작일·종료일 누락: {festival_date_missing}")
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
    parser.add_argument(
        "--if-empty",
        action="store_true",
        help="DB가 비어 있을 때만 적재합니다. 일반 실행은 기존 데이터를 갱신하는 upsert입니다.",
    )
    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)
    ensure_tour_content_event_columns()
    settings = get_settings()
    data_directory = args.data_dir or settings.data_directory

    with SessionLocal() as db:
        current = db.scalar(select(func.count(TourContent.id))) or 0
        if args.if_empty and current > 0:
            print(f"기존 데이터 {current}건이 있어 적재를 건너뜁니다.")
            validate_database(db)
            return
        inserted, updated = seed_all_json_files(db, data_directory)
        print(f"신규 적재: {inserted}건 / 갱신: {updated}건")
        validate_database(db)


if __name__ == "__main__":
    main()
