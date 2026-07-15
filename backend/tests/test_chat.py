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


def test_chat_limitations(client):
    festival = client.post(
        "/api/chat",
        json={"message": "이번 주말에 열리는 축제 알려줘", "history": []},
    ).json()
    assert festival["intent"] == "LIMITATION"
    assert "시작일" in festival["answer"]

    restaurant = client.post(
        "/api/chat",
        json={"message": "여수 모범음식점 알려줘", "history": []},
    ).json()
    assert restaurant["intent"] == "LIMITATION"
    assert "지정 여부" in restaurant["answer"]
