from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/api/config", tags=["config"])


@router.get("/public")
def public_config():
    """브라우저에서 사용 가능한 공개 설정만 반환한다.

    Kakao JavaScript 키는 브라우저 SDK 로드 시 원래 공개되는 값이며,
    카카오 개발자 콘솔의 허용 도메인으로 사용 범위를 제한해야 한다.
    """
    settings = get_settings()
    return {
        "kakaoMapAppKey": settings.kakao_map_app_key.strip(),
        "openweatherConfigured": bool(settings.openweather_api_key.strip()),
    }
