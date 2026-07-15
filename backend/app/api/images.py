from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException, Query, Response

router = APIRouter(prefix="/api/images", tags=["images"])
ALLOWED_HOSTS = {"tong.visitkorea.or.kr"}


@router.get("/proxy")
async def proxy_image(url: str = Query(..., min_length=10)):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or parsed.hostname not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="허용되지 않은 이미지 주소입니다.")
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
            upstream = await client.get(url)
            upstream.raise_for_status()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail="원본 이미지를 불러오지 못했습니다.") from exc

    content_type = upstream.headers.get("content-type", "image/jpeg")
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=502, detail="이미지 응답이 아닙니다.")
    return Response(
        content=upstream.content,
        media_type=content_type,
        headers={"Cache-Control": "public, max-age=86400"},
    )
