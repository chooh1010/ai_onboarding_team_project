from types import SimpleNamespace

from app.api import weather


class FakeResponse:
    status_code = 200
    text = ""

    def json(self):
        return {
            "weather": [{"main": "Clear"}],
            "main": {"temp": 23.4},
        }


class FakeAsyncClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False

    async def get(self, *args, **kwargs):
        return FakeResponse()


def test_current_weather_uses_configured_regions(client, monkeypatch):
    monkeypatch.setattr(
        weather,
        "get_settings",
        lambda: SimpleNamespace(openweather_api_key="test-key"),
    )
    monkeypatch.setattr(weather.httpx, "AsyncClient", FakeAsyncClient)
    weather._weather_cache["current"] = {
        "expires_at": weather.datetime.min.replace(tzinfo=weather.timezone.utc),
        "data": None,
    }

    response = client.get("/api/weather/current")

    assert response.status_code == 200
    body = response.json()
    assert len(body) == len(weather.GWANGJU_JEONBUK_JEONNAM_REGIONS)
    assert body[0]["region_name"] == "광주"
    assert body[0]["temp"] == 23.4


def test_public_config_endpoint(client):
    response = client.get("/api/config/public")

    assert response.status_code == 200
    body = response.json()
    assert "kakaoMapAppKey" in body
    assert "openweatherConfigured" in body
