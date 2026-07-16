import os
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./test_regional_tour.db"
os.environ["OPENAI_API_KEY"] = ""

import pytest
from fastapi.testclient import TestClient

from app.core.database import Base, SessionLocal, engine
from app.main import app
from app.models import Post, TourContent

TEST_DB = Path("test_regional_tour.db")


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        db.add_all(
            [
                TourContent(
                    content_id="132880",
                    content_type_id="39",
                    content_type_name="음식점",
                    region_group="광주_전라권",
                    source_file="test.json",
                    title="제일반점",
                    addr1="전남광주통합특별시 동구 구성로 174",
                    addr2="",
                    zipcode="61481",
                    tel="",
                    mapx="126.9125968520",
                    mapy="35.1515409291",
                    mlevel="6",
                    area_code="5",
                    sigungu_code="3",
                    ldong_regn_cd="12",
                    ldong_signgu_cd="210",
                    cat1="A05",
                    cat2="A0502",
                    cat3="A05020400",
                    lcls_system1="FD",
                    lcls_system2="FD02",
                    lcls_system3="FD020100",
                    first_image="http://tong.visitkorea.or.kr/image.jpg",
                    first_image2="",
                    copyright_code="Type3",
                    source_created_time="",
                    source_modified_time="",
                    raw_json="{}",
                ),
                TourContent(
                    content_id="999001",
                    content_type_id="39",
                    content_type_name="음식점",
                    region_group="광주_전라권",
                    source_file="test.json",
                    title="서구 테스트 식당",
                    addr1="전남광주통합특별시 서구",
                    addr2="",
                    zipcode="",
                    tel="",
                    mapx="126.8500",
                    mapy="35.1500",
                    mlevel="6",
                    area_code="5",
                    sigungu_code="5",
                    ldong_regn_cd="",
                    ldong_signgu_cd="",
                    cat1="",
                    cat2="",
                    cat3="",
                    lcls_system1="",
                    lcls_system2="",
                    lcls_system3="",
                    first_image="",
                    first_image2="",
                    copyright_code="",
                    source_created_time="",
                    source_modified_time="",
                    raw_json="{}",
                ),
                TourContent(
                    content_id="1874417",
                    content_type_id="32",
                    content_type_name="숙박",
                    region_group="광주_전라권",
                    source_file="test.json",
                    title="테스트 호텔",
                    addr1="전북특별자치도 전주시 완산구",
                    addr2="",
                    zipcode="",
                    tel="",
                    mapx="127.1480",
                    mapy="35.8242",
                    mlevel="6",
                    area_code="37",
                    sigungu_code="12",
                    ldong_regn_cd="",
                    ldong_signgu_cd="",
                    cat1="",
                    cat2="",
                    cat3="",
                    lcls_system1="",
                    lcls_system2="",
                    lcls_system3="",
                    first_image="",
                    first_image2="",
                    copyright_code="",
                    source_created_time="",
                    source_modified_time="",
                    raw_json="{}",
                ),
                TourContent(
                    content_id="3569001",
                    content_type_id="15",
                    content_type_name="축제공연행사",
                    region_group="광주_전라권",
                    source_file="test.json",
                    title="전주 가맥축제",
                    addr1="전북특별자치도 전주시 완산구 천잠로 303",
                    addr2="",
                    zipcode="",
                    tel="",
                    mapx="127.1000",
                    mapy="35.8000",
                    mlevel="6",
                    area_code="37",
                    sigungu_code="12",
                    ldong_regn_cd="",
                    ldong_signgu_cd="",
                    cat1="A02",
                    cat2="A0208",
                    cat3="A02081300",
                    lcls_system1="EV",
                    lcls_system2="EV03",
                    lcls_system3="EV030400",
                    first_image="",
                    first_image2="",
                    copyright_code="Type3",
                    source_created_time="",
                    source_modified_time="",
                    event_start_date="20260806",
                    event_end_date="20260808",
                    event_place="전주대학교 대운동장",
                    playtime="16:00~22:00",
                    use_time_festival="무료",
                    raw_json="{}",
                ),
            ]
        )
        db.add(
            Post(
                category="FOOD",
                title="떡갈비 추천",
                content="광주 떡갈비 추천 부탁드립니다.",
                edit_password="1234",
            )
        )
        db.commit()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
