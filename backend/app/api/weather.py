import asyncio
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings

router = APIRouter(prefix="/api/weather", tags=["weather"])

# 서비스가 제공하는 광주·전라권 11개 주요 지역 좌표
GWANGJU_JEONBUK_JEONNAM_REGIONS = {
    "광주": (35.1595, 126.8526),
    "담양": (35.3214, 126.9882),
    "나주": (35.0159, 126.7108),
    "화순": (35.0645, 126.9865),
    "장성": (35.3019, 126.7849),
    "여수": (34.7604, 127.6622),
    "해남": (34.5734, 126.5992),
    "진도": (34.4868, 126.2635),
    "순천": (34.9505, 127.4872),
    "전주": (35.8242, 127.1480),
    "남원": (35.4164, 127.3904),
}

CACHE_TTL = timedelta(minutes=15)
_weather_cache = {
    "current": {"expires_at": datetime.min.replace(tzinfo=timezone.utc), "data": None},
    "forecast": {"expires_at": datetime.min.replace(tzinfo=timezone.utc), "data": None},
}

OPENWEATHER_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
OPENWEATHER_AIR_URL = "https://api.openweathermap.org/data/2.5/air_pollution"


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _check_cache(key: str):
    entry = _weather_cache[key]
    if entry["data"] is not None and entry["expires_at"] > _now_utc():
        return entry["data"]
    return None


def _set_cache(key: str, data):
    _weather_cache[key]["data"] = data
    _weather_cache[key]["expires_at"] = _now_utc() + CACHE_TTL


def _parse_weather_state(weather_list: list[dict]) -> str:
    if not weather_list:
        return "Clear"
    return weather_list[0].get("main", "Clear")


def _get_air_quality_flag(data: dict) -> bool:
    components = data.get("list", [{}])[0].get("components", {})
    pm25 = components.get("pm2_5", 0)
    return pm25 >= 35


def _upstream_error_message(response: httpx.Response) -> str:
    try:
        body = response.json()
        return str(body.get("message") or response.text)
    except ValueError:
        return response.text


def _group_daily_forecast(items: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for item in items:
        timestamp = item.get("dt")
        if timestamp is None:
            continue
        day = datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
        bucket = grouped.setdefault(
            day,
            {
                "minTemp": float("inf"),
                "maxTemp": float("-inf"),
                "conditions": [],
                "hasRain": False,
            },
        )

        temp = item.get("main", {}).get("temp")
        if temp is not None:
            bucket["minTemp"] = min(bucket["minTemp"], temp)
            bucket["maxTemp"] = max(bucket["maxTemp"], temp)

        conditions = item.get("weather", [])
        if conditions:
            bucket["conditions"].append(conditions[0].get("main"))

        if item.get("rain") or item.get("snow"):
            bucket["hasRain"] = True
        elif conditions and conditions[0].get("main") in ["Rain", "Snow", "Thunderstorm"]:
            bucket["hasRain"] = True

    weekday_labels = ["월", "화", "수", "목", "금", "토", "일"]
    forecast = []

    for day_label, data in grouped.items():
        date_obj = datetime.strptime(day_label, "%Y-%m-%d")
        condition = "Clear"
        if data["conditions"]:
            condition = max(set(data["conditions"]), key=data["conditions"].count)
        forecast.append(
            {
                "dayOfWeek": weekday_labels[date_obj.weekday()],
                "date": date_obj.strftime("%m/%d"),
                "state": condition,
                "minTemp": int(round(data["minTemp"])) if data["minTemp"] != float("inf") else 0,
                "maxTemp": int(round(data["maxTemp"])) if data["maxTemp"] != float("-inf") else 0,
                "hasRain": data["hasRain"],
                "_sort_date": date_obj,
            }
        )

    sorted_forecast = sorted(forecast, key=lambda item: item["_sort_date"])
    return [
        {key: value for key, value in item.items() if key != "_sort_date"}
        for item in sorted_forecast
    ]


@router.get("/current")
async def current_region_weather():
    settings = get_settings()
    key = settings.openweather_api_key.strip()
    if not key:
        raise HTTPException(status_code=503, detail="OPENWEATHER_API_KEY가 설정되지 않았습니다.")

    cached = _check_cache("current")
    if cached is not None:
        return cached

    async with httpx.AsyncClient(timeout=12.0) as client:
        tasks = [
            client.get(
                OPENWEATHER_CURRENT_URL,
                params={"lat": lat, "lon": lon, "units": "metric", "appid": key},
            )
            for lat, lon in GWANGJU_JEONBUK_JEONNAM_REGIONS.values()
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    results = []
    failures = []
    for region, response in zip(GWANGJU_JEONBUK_JEONNAM_REGIONS.keys(), responses):
        if isinstance(response, Exception):
            failures.append(f"{region}: {response}")
            continue
        if response.status_code != 200:
            failures.append(f"{region}: {_upstream_error_message(response)}")
            continue

        data = response.json()
        results.append(
            {
                "region_name": region,
                "weather_state": _parse_weather_state(data.get("weather", [])),
                "temp": data.get("main", {}).get("temp"),
            }
        )

    if not results:
        detail = failures[0] if failures else "OpenWeather 응답을 받지 못했습니다."
        raise HTTPException(status_code=502, detail=f"현재 날씨 조회 실패: {detail}")

    _set_cache("current", results)
    return results


@router.get("/forecast")
async def weekly_forecast(area: str = "광주·전라권"):
    del area  # 현재는 권역 대표 좌표를 사용한다.
    settings = get_settings()
    key = settings.openweather_api_key.strip()
    if not key:
        raise HTTPException(status_code=503, detail="OPENWEATHER_API_KEY가 설정되지 않았습니다.")

    cached = _check_cache("forecast")
    if cached is not None:
        return cached

    # 광주·전라권 중간 지점의 대표 예보
    lat, lon = 35.15, 127.0
    async with httpx.AsyncClient(timeout=15.0) as client:
        forecast_req = client.get(
            OPENWEATHER_FORECAST_URL,
            params={"lat": lat, "lon": lon, "units": "metric", "appid": key},
        )
        air_req = client.get(
            OPENWEATHER_AIR_URL,
            params={"lat": lat, "lon": lon, "appid": key},
        )
        forecast_resp, air_resp = await asyncio.gather(forecast_req, air_req)

    if forecast_resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"예보 조회 실패: {_upstream_error_message(forecast_resp)}",
        )

    if air_resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"대기질 조회 실패: {_upstream_error_message(air_resp)}",
        )

    days = _group_daily_forecast(forecast_resp.json().get("list", []))[:5]
    has_dust = _get_air_quality_flag(air_resp.json())

    result = {"items": [{**day, "has_dust": has_dust} for day in days]}
    _set_cache("forecast", result)
    return result
