from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException
from app.core.config import get_settings
import httpx
import asyncio

router = APIRouter(prefix="/api/weather", tags=["weather"])

# Jeonnam (South Jeolla Province) major cities coordinates
JEONNAM_REGIONS = {
    "여수": (34.7604, 127.6622),
    "순천": (34.9505, 127.4895),
    "담양": (35.3428, 126.9915),
    "나주": (34.9993, 126.7040),
    "화순": (35.2303, 126.9770),
    "장성": (35.3268, 126.7750),
    "해남": (34.5500, 126.6000),
    "진도": (34.3800, 126.2500),
}

CACHE_TTL = timedelta(minutes=15)
_weather_cache = {
    "current": {"expires_at": datetime.min, "data": None},
    "forecast": {"expires_at": datetime.min, "data": None},
}

OPENWEATHER_CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
OPENWEATHER_AIR_URL = "https://api.openweathermap.org/data/2.5/air_pollution"


def _check_cache(key: str):
    entry = _weather_cache[key]
    if entry["data"] is not None and entry["expires_at"] > datetime.utcnow():
        return entry["data"]
    return None


def _set_cache(key: str, data):
    _weather_cache[key]["data"] = data
    _weather_cache[key]["expires_at"] = datetime.utcnow() + CACHE_TTL


def _parse_weather_state(weather_list: list[dict]) -> str:
    if not weather_list:
        return "Clear"
    return weather_list[0].get("main", "Clear")


def _get_air_quality_flag(data: dict) -> bool:
    components = data.get("list", [{}])[0].get("components", {})
    pm25 = components.get("pm2_5", 0)
    return pm25 >= 35


def _group_daily_forecast(items: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = {}
    for item in items:
        timestamp = item.get("dt")
        if timestamp is None:
            continue
        day = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")
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

    weekday_labels = ["月", "火", "水", "木", "金", "土", "日"]

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
        {
            key: value
            for key, value in item.items()
            if key != "_sort_date"
        }
        for item in sorted_forecast
    ]


@router.get("/current")
async def current_region_weather():
    settings = get_settings()
    key = settings.openweather_api_key
    if not key:
        raise HTTPException(status_code=503, detail="OpenWeather API key not configured")

    cached = _check_cache("current")
    if cached is not None:
        return cached

    async with httpx.AsyncClient(timeout=10.0) as client:
        tasks = []
        for region, (lat, lon) in GWANGJU_REGIONS.items():
            params = {
                "lat": lat,
                "lon": lon,
                "units": "metric",
                "appid": key,
            }
            tasks.append(client.get(OPENWEATHER_CURRENT_URL, params=params))

        responses = await asyncio.gather(*tasks)

    results = []
    for region, resp in zip(GWANGJU_REGIONS.keys(), responses):
        if resp.status_code != 200:
            try:
                err = resp.json()
                message = err.get("message") or resp.text
            except ValueError:
                message = resp.text
            raise HTTPException(status_code=502, detail=f"Failed to fetch current weather for {region}: {message}")

        data = resp.json()
        results.append(
            {
                "region_name": region,
                "weather_state": _parse_weather_state(data.get("weather", [])),
                "temp": data.get("main", {}).get("temp"),
            }
        )

    _set_cache("current", results)
    return results


@router.get("/forecast")
async def weekly_forecast(area: str = "전라남도"):
    settings = get_settings()
    key = settings.openweather_api_key
    if not key:
        raise HTTPException(status_code=503, detail="OpenWeather API key not configured")

    cached = _check_cache("forecast")
    if cached is not None:
        return cached

    # Center of South Jeolla Province (near Yeosu/Suncheon area)
    lat, lon = 34.8, 127.0
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
        try:
            err = forecast_resp.json()
            message = err.get("message") or forecast_resp.text
        except ValueError:
            message = forecast_resp.text
        raise HTTPException(status_code=502, detail=f"Failed to fetch forecast data: {message}")

    if air_resp.status_code != 200:
        try:
            err = air_resp.json()
            message = err.get("message") or air_resp.text
        except ValueError:
            message = air_resp.text
        raise HTTPException(status_code=502, detail=f"Failed to fetch air quality data: {message}")

    forecast_data = forecast_resp.json()
    air_data = air_resp.json()

    days = _group_daily_forecast(forecast_data.get("list", []))[:7]
    has_dust = _get_air_quality_flag(air_data)

    result = {"items": [{**day, "has_dust": has_dust} for day in days]}
    _set_cache("forecast", result)
    return result
