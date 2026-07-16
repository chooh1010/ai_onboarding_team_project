def test_content_type_counts(client):
    response = client.get("/api/content-types")
    assert response.status_code == 200
    counts = {item["id"]: item["count"] for item in response.json()["items"]}
    assert counts == {"15": 1, "32": 1, "39": 2}


def test_filter_yeosu_like_query_and_detail(client):
    response = client.get(
        "/api/contents",
        params={"contentTypeId": "39", "areaCode": "5", "sigunguCode": "3"},
    )
    assert response.status_code == 200
    assert response.json()["totalElements"] == 1
    assert response.json()["items"][0]["contentId"] == "132880"

    detail = client.get("/api/contents/132880")
    assert detail.status_code == 200
    assert detail.json()["title"] == "제일반점"
    assert detail.json()["source"]["license"] == "공공누리 제3유형"


def test_festival_date_overlap_filter_and_detail(client):
    response = client.get(
        "/api/contents",
        params={
            "contentTypeId": "15",
            "areaCode": "37",
            "sigunguCode": "12",
            "queryStartDate": "20260807",
            "queryEndDate": "20260807",
            "sort": "event-date",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["totalElements"] == 1
    assert body["items"][0]["eventStartDate"] == "20260806"
    assert body["items"][0]["eventEndDate"] == "20260808"

    detail = client.get("/api/contents/3569001")
    assert detail.status_code == 200
    assert detail.json()["eventPlace"] == "전주대학교 대운동장"
    assert detail.json()["playtime"] == "16:00~22:00"


def test_not_found(client):
    response = client.get("/api/contents/not-exists")
    assert response.status_code == 404
