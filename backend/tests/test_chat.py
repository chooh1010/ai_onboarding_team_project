def test_chat_search_fallback(client):
    response = client.post(
        "/api/chat",
        json={"message": "광주 동구 음식점 알려줘", "history": []},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "TOUR_CONTENT_SEARCH"
    assert [item["title"] for item in data["results"]] == ["제일반점"]
    assert data["usedOpenai"] is False


def test_chat_searches_festival_by_event_date(client):
    festival = client.post(
        "/api/chat",
        json={"message": "2026년 8월 7일 전주 축제 알려줘", "history": []},
    )
    assert festival.status_code == 200
    data = festival.json()
    assert data["intent"] == "TOUR_CONTENT_SEARCH"
    assert [item["title"] for item in data["results"]] == ["전주 가맥축제"]
    assert data["results"][0]["eventStartDate"] == "20260806"
    assert data["results"][0]["eventEndDate"] == "20260808"
    assert "2026년 8월 6일부터 2026년 8월 8일까지" in data["answer"]


def test_chat_limitations(client):
    restaurant = client.post(
        "/api/chat",
        json={"message": "여수 모범음식점 알려줘", "history": []},
    ).json()
    assert restaurant["intent"] == "LIMITATION"
    assert "지정 여부" in restaurant["answer"]
