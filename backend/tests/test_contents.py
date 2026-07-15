def test_content_type_counts(client):
    response = client.get("/api/content-types")
    assert response.status_code == 200
    counts = {item["id"]: item["count"] for item in response.json()["items"]}
    assert counts == {"32": 1, "39": 2}


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


def test_not_found(client):
    response = client.get("/api/contents/not-exists")
    assert response.status_code == 404
