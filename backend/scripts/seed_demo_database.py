import json

from sqlalchemy import select

from app.core.database import Base, SessionLocal, engine
from app.models.tour_content import TourContent

DEMO_ITEMS = [
    {
        "contentid": "132880",
        "contenttypeid": "39",
        "contentType": "음식점",
        "title": "제일반점",
        "addr1": "전남광주통합특별시 동구 구성로 174",
        "addr2": "",
        "areacode": "5",
        "sigungucode": "3",
        "mapx": "126.9125968520",
        "mapy": "35.1515409291",
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/80/3029180_image2_1.jpg",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/80/3029180_image3_1.jpg",
        "cpyrhtDivCd": "Type3",
    },
    {
        "contentid": "134997",
        "contenttypeid": "39",
        "contentType": "음식점",
        "title": "송정떡갈비 1호점",
        "addr1": "전남광주통합특별시 광산구 광산로29번길 1",
        "addr2": "",
        "areacode": "5",
        "sigungucode": "1",
        "mapx": "126.7948298032",
        "mapy": "35.1389542543",
        "firstimage": "",
        "firstimage2": "",
        "cpyrhtDivCd": "",
    },
    {
        "contentid": "1074432",
        "contenttypeid": "12",
        "contentType": "관광지",
        "title": "무등산 주상절리대",
        "addr1": "전남광주통합특별시 동구 용연동",
        "addr2": "산 354-1",
        "areacode": "5",
        "sigungucode": "3",
        "mapx": "126.9990150009",
        "mapy": "35.1202403693",
        "firstimage": "",
        "firstimage2": "",
        "cpyrhtDivCd": "Type3",
    },
    {
        "contentid": "1874417",
        "contenttypeid": "32",
        "contentType": "숙박",
        "title": "호텔 5월 (Hotel The May)",
        "addr1": "전남광주통합특별시 서구 상무번영로 51",
        "addr2": "(치평동)",
        "areacode": "5",
        "sigungucode": "5",
        "mapx": "126.8527770650",
        "mapy": "35.1545895749",
        "firstimage": "",
        "firstimage2": "",
        "cpyrhtDivCd": "",
    },
    {
        "contentid": "3460731",
        "contenttypeid": "15",
        "contentType": "축제공연행사",
        "title": "광주여성영화제",
        "addr1": "전남광주통합특별시 동구 중앙로160번길 16-7 (불로동)",
        "addr2": "",
        "areacode": "5",
        "sigungucode": "3",
        "mapx": "126.9146634529",
        "mapy": "35.1468609363",
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/26/3460726_image2_1.jpg",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/26/3460726_image3_1.jpg",
        "cpyrhtDivCd": "Type3",
    },
    {
        "contentid": "2666784",
        "contenttypeid": "25",
        "contentType": "여행코스",
        "title": "활기가 넘치면서도 치열한 가슴을 품어 아름다운 광주 속으로!",
        "addr1": "전남광주통합특별시 동구 지호로164번길 35-1",
        "addr2": "(지산동)",
        "areacode": "5",
        "sigungucode": "3",
        "mapx": "126.9491103443",
        "mapy": "35.1494112311",
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/94/2563694_image2_1.jpg",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/94/2563694_image2_1.jpg",
        "cpyrhtDivCd": "Type3",
    },
    {
        "contentid": "1622267",
        "contenttypeid": "28",
        "contentType": "레포츠",
        "title": "염주실내수영장",
        "addr1": "전남광주통합특별시 서구 금화로 278",
        "addr2": "(풍암동)",
        "areacode": "5",
        "sigungucode": "5",
        "mapx": "126.8791807340",
        "mapy": "35.1366531569",
        "firstimage": "http://tong.visitkorea.or.kr/cms/resource/14/1587814_image2_1.jpg",
        "firstimage2": "http://tong.visitkorea.or.kr/cms/resource/14/1587814_image3_1.jpg",
        "cpyrhtDivCd": "Type3",
    },
]


def main():
    Base.metadata.create_all(bind=engine)
    inserted = 0
    with SessionLocal() as db:
        for item in DEMO_ITEMS:
            if db.scalar(select(TourContent.id).where(TourContent.content_id == item["contentid"])):
                continue
            db.add(
                TourContent(
                    content_id=item["contentid"],
                    content_type_id=item["contenttypeid"],
                    content_type_name=item["contentType"],
                    region_group="광주_전라권",
                    source_file="demo_data",
                    title=item["title"],
                    addr1=item["addr1"],
                    addr2=item["addr2"],
                    zipcode="",
                    tel="",
                    mapx=item["mapx"],
                    mapy=item["mapy"],
                    mlevel="6",
                    area_code=item["areacode"],
                    sigungu_code=item["sigungucode"],
                    ldong_regn_cd="",
                    ldong_signgu_cd="",
                    cat1="",
                    cat2="",
                    cat3="",
                    lcls_system1="",
                    lcls_system2="",
                    lcls_system3="",
                    first_image=item["firstimage"],
                    first_image2=item["firstimage2"],
                    copyright_code=item["cpyrhtDivCd"],
                    source_created_time="",
                    source_modified_time="",
                    raw_json=json.dumps(item, ensure_ascii=False),
                )
            )
            inserted += 1
        db.commit()
    print(f"데모 데이터 {inserted}건 적재 완료")


if __name__ == "__main__":
    main()
