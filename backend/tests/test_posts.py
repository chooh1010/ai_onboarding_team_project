def test_post_crud_and_password_not_exposed(client):
    created = client.post(
        "/api/posts",
        json={
            "category": "FOOD",
            "title": "여수 음식점 추천해주세요",
            "content": "가족 여행 중입니다.",
            "password": "5678",
        },
    )
    assert created.status_code == 201
    data = created.json()
    assert "password" not in data
    assert "editPassword" not in data
    post_id = data["id"]

    wrong = client.put(
        f"/api/posts/{post_id}",
        json={"title": "수정 제목", "content": "수정", "password": "0000"},
    )
    assert wrong.status_code == 403

    updated = client.put(
        f"/api/posts/{post_id}",
        json={"title": "수정 제목", "content": "수정 내용", "password": "5678"},
    )
    assert updated.status_code == 200
    assert updated.json()["title"] == "수정 제목"

    deleted = client.request(
        "DELETE",
        f"/api/posts/{post_id}",
        json={"password": "5678"},
    )
    assert deleted.status_code == 204
