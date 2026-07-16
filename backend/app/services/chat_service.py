import calendar
import re
from datetime import date, datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.content_repository import ContentRepository
from app.repositories.post_repository import PostRepository
from app.schemas.chat import ChatRequest, ChatResponse, ChatResult
from app.services.content_service import ContentService
from app.services.openai_service import OpenAIService
from app.services.post_service import PostService


CONTENT_TYPES = {
    "관광지": "12",
    "관광": "12",
    "문화시설": "14",
    "문화": "14",
    "축제": "15",
    "공연": "15",
    "행사": "15",
    "여행코스": "25",
    "코스": "25",
    "레포츠": "28",
    "숙박": "32",
    "호텔": "32",
    "펜션": "32",
    "쇼핑": "38",
    "시장": "38",
    "음식점": "39",
    "맛집": "39",
    "식당": "39",
}

AREAS = {
    "광주": ("5", None),
    "광산구": ("5", "1"),
    "남구": ("5", "2"),
    "동구": ("5", "3"),
    "북구": ("5", "4"),
    "서구": ("5", "5"),
    "담양": ("38", "7"),
    "나주": ("38", "6"),
    "화순": ("38", "24"),
    "장성": ("38", "19"),
    "여수": ("38", "13"),
    "해남": ("38", "23"),
    "진도": ("38", "21"),
    "순천": ("38", "11"),
    "전주": ("37", "12"),
    "남원": ("37", "4"),
}

CATEGORY_BY_CONTENT_TYPE = {
    "12": "TOURISM",
    "39": "FOOD",
    "32": "LODGING",
    "15": "FESTIVAL",
    "25": "COURSE",
}


class ChatService:
    def __init__(self, db: Session):
        self.content_service = ContentService(ContentRepository(db))
        self.post_service = PostService(PostRepository(db))
        self.openai_service = OpenAIService(get_settings())

    async def answer(self, request: ChatRequest) -> ChatResponse:
        limitation = self._limitation_response(request.message)
        if limitation:
            return limitation

        if self.openai_service.enabled:
            try:
                answer, tool_name, tool_result = await self.openai_service.answer(
                    message=request.message,
                    history=[item.model_dump() for item in request.history],
                    tool_handlers=self._tool_handlers(),
                )
                results = self._results_from_tool(tool_name, tool_result)
                return ChatResponse(
                    answer=answer,
                    intent=self._intent_from_tool(tool_name),
                    results=results,
                    used_openai=True,
                )
            except Exception:
                # API 장애나 키/모델 설정 오류 시 반드시 검색 fallback으로 전환
                pass

        return await self._fallback(request.message)

    def _tool_handlers(self):
        async def search_tour_contents(**kwargs):
            limit = kwargs.pop("limit", 5)
            has_date_filter = bool(
                kwargs.get("query_start_date") or kwargs.get("query_end_date")
            )
            response = self.content_service.list_contents(
                page=1,
                size=limit,
                sort="event-date" if has_date_filter else "title",
                **kwargs,
            )
            return response.model_dump(by_alias=True)

        async def search_nearby_contents(**kwargs):
            items = self.content_service.nearby(**kwargs)
            return {"items": [item.model_dump(by_alias=True) for item in items]}

        async def search_community_posts(**kwargs):
            limit = kwargs.pop("limit", 5)
            response = self.post_service.list_posts(page=1, size=limit, **kwargs)
            return response.model_dump(by_alias=True)

        async def get_tour_content(content_id: str):
            detail = self.content_service.get_detail(content_id)
            return detail.model_dump(by_alias=True) if detail else {"error": "not_found"}

        async def get_data_source():
            return {
                "provider": "한국관광공사",
                "dataset": "국문 관광정보 서비스",
                "api": "TourAPI 4.0",
                "license": "공공누리 제3유형",
                "collectedAt": None,
            }

        return {
            "search_tour_contents": search_tour_contents,
            "search_nearby_contents": search_nearby_contents,
            "search_community_posts": search_community_posts,
            "get_tour_content": get_tour_content,
            "get_data_source": get_data_source,
        }

    async def _fallback(self, message: str) -> ChatResponse:
        if any(word in message for word in ["출처", "라이선스", "데이터 어디"]):
            return ChatResponse(
                answer=(
                    "이 서비스는 한국관광공사 국문 관광정보 서비스(TourAPI 4.0) "
                    "데이터를 사용합니다. 라이선스는 공공누리 제3유형이며, "
                    "상업적 이용은 가능하지만 원본 데이터 내용 변경은 금지됩니다.\n\n"
                    "출처: 한국관광공사 TourAPI 4.0 / 라이선스: 공공누리 제3유형"
                ),
                intent="DATA_SOURCE",
            )

        content_type_id = self._find_content_type(message)
        area_code, sigungu_code = self._find_area(message)

        if any(word in message for word in ["커뮤니티", "게시글", "관련 글", "글 찾아"]):
            keyword = self._extract_keyword(message)
            category = CATEGORY_BY_CONTENT_TYPE.get(content_type_id)
            posts = self.post_service.list_posts(
                category=category,
                keyword=keyword or None,
                page=1,
                size=5,
            )
            results = [
                ChatResult(
                    post_id=post.id,
                    type="커뮤니티",
                    title=post.title,
                )
                for post in posts.items
            ]
            answer = (
                f"관련 커뮤니티 글 {len(results)}건을 찾았습니다."
                if results
                else "조건에 맞는 커뮤니티 글을 찾지 못했습니다."
            )
            return ChatResponse(answer=answer, intent="COMMUNITY_SEARCH", results=results)

        date_range = self._extract_date_range(message)
        keyword = self._extract_keyword(message)
        query_start_date = date_range[0].strftime("%Y%m%d") if date_range else None
        query_end_date = date_range[1].strftime("%Y%m%d") if date_range else None

        response = self.content_service.list_contents(
            content_type_id=content_type_id,
            area_code=area_code,
            sigungu_code=sigungu_code,
            keyword=keyword or None,
            has_image=None,
            query_start_date=query_start_date,
            query_end_date=query_end_date,
            page=1,
            size=5,
            sort="event-date" if date_range else "title",
        )
        results = [
            ChatResult(
                content_id=item.content_id,
                type=item.content_type_name,
                title=item.title,
                address=item.address,
                image_url=item.thumbnail_url,
                event_start_date=item.event_start_date,
                event_end_date=item.event_end_date,
                event_place=item.event_place,
            )
            for item in response.items
        ]
        location_name = next(
            (name for name, codes in AREAS.items() if codes == (area_code, sigungu_code)),
            "광주·전라권",
        )
        type_name = next(
            (
                name
                for name, code in CONTENT_TYPES.items()
                if code == content_type_id and len(name) >= 3
            ),
            "관광 콘텐츠",
        )

        if content_type_id == "15":
            if date_range:
                period_label = self._format_date_range(*date_range)
                answer = (
                    f"{period_label}에 진행되는 {location_name}의 축제·행사 "
                    f"{len(results)}건을 찾았습니다."
                    if results
                    else f"{period_label}에 진행되는 {location_name}의 축제·행사를 찾지 못했습니다."
                )
            else:
                answer = (
                    f"{location_name}의 축제·행사 {len(results)}건을 찾았습니다."
                    if results
                    else "조건에 맞는 축제·행사를 찾지 못했습니다."
                )
            if results:
                details = []
                for result in results:
                    event_period = self._format_event_period(
                        result.event_start_date,
                        result.event_end_date,
                    )
                    place = result.event_place or result.address or "장소 정보 없음"
                    details.append(f"- {result.title}: {event_period} · {place}")
                answer += "\n" + "\n".join(details)
        else:
            answer = (
                f"{location_name}의 {type_name} {len(results)}곳을 찾았습니다."
                if results
                else "조건에 맞는 관광 콘텐츠를 찾지 못했습니다."
            )

        answer += "\n\n출처: 한국관광공사 TourAPI 4.0 / 라이선스: 공공누리 제3유형"
        return ChatResponse(answer=answer, intent="TOUR_CONTENT_SEARCH", results=results)

    @staticmethod
    def _limitation_response(message: str) -> ChatResponse | None:
        if "모범음식점" in message or "위생등급" in message:
            text = (
                "현재 제공된 음식점 데이터에는 모범음식점 지정 여부나 위생등급이 "
                "포함되어 있지 않습니다. 대신 해당 지역의 등록 음식점 목록은 안내할 수 있습니다."
            )
            return ChatResponse(
                answer=text,
                intent="LIMITATION",
                limitations=["모범음식점 지정 여부·위생등급 필드 없음"],
            )
        if "코스" in message and any(
            word in message for word in ["순서", "경로", "이동 시간", "총 거리", "교통수단"]
        ):
            text = (
                "현재 여행코스 데이터에는 코스 구성 장소, 방문 순서, 이동 시간, "
                "총 거리와 교통수단이 없어 상세 경로를 만들 수 없습니다."
            )
            return ChatResponse(
                answer=text,
                intent="LIMITATION",
                limitations=["여행코스 구성 장소·순서·거리 필드 없음"],
            )
        return None

    @staticmethod
    def _find_content_type(message: str) -> str | None:
        for keyword, content_type_id in CONTENT_TYPES.items():
            if keyword in message:
                return content_type_id
        return None

    @staticmethod
    def _find_area(message: str) -> tuple[str | None, str | None]:
        # "광주 동구"처럼 광역시와 구가 함께 있으면 구 조건을 우선한다.
        for district in ["광산구", "남구", "동구", "북구", "서구"]:
            if district in message and ("광주" in message or district == "광산구"):
                return AREAS[district]
        for keyword in [
            "담양",
            "나주",
            "화순",
            "장성",
            "여수",
            "해남",
            "진도",
            "순천",
            "전주",
            "남원",
            "광주",
        ]:
            if keyword in message:
                return AREAS[keyword]
        return None, None

    @staticmethod
    def _extract_keyword(message: str) -> str:
        cleaned = message
        cleaned = re.sub(r"\d{4}\s*년\s*\d{1,2}\s*월(?:\s*\d{1,2}\s*일)?", " ", cleaned)
        cleaned = re.sub(r"\d{4}[./-]\d{1,2}[./-]\d{1,2}", " ", cleaned)
        cleaned = re.sub(r"\d{1,2}\s*월\s*\d{1,2}\s*일", " ", cleaned)
        cleaned = re.sub(r"\d{1,2}\s*월", " ", cleaned)
        stopwords = list(CONTENT_TYPES) + list(AREAS) + [
            "커뮤니티",
            "게시글",
            "관련",
            "글",
            "찾아줘",
            "검색해줘",
            "알려줘",
            "추천해줘",
            "언제",
            "일정",
            "기간",
            "오늘",
            "이번 주말",
            "이번 달",
            "진행 중",
            "진행 중인",
            "열리는",
            "개최되는",
            "있는",
        ]
        for word in sorted(stopwords, key=len, reverse=True):
            cleaned = cleaned.replace(word, " ")
        cleaned = re.sub(r"[^0-9A-Za-z가-힣]+", " ", cleaned)
        return " ".join(cleaned.split())

    @staticmethod
    def _extract_date_range(
        message: str,
        today: date | None = None,
    ) -> tuple[date, date] | None:
        today = today or datetime.now(ZoneInfo("Asia/Seoul")).date()

        full_dates = re.findall(
            r"(\d{4})\s*년\s*(\d{1,2})\s*월\s*(\d{1,2})\s*일",
            message,
        )
        parsed_full = ChatService._valid_dates(full_dates)
        if parsed_full:
            return min(parsed_full), max(parsed_full)

        iso_dates = re.findall(
            r"(?<!\d)(\d{4})[./-](\d{1,2})[./-](\d{1,2})(?!\d)",
            message,
        )
        parsed_iso = ChatService._valid_dates(iso_dates)
        if parsed_iso:
            return min(parsed_iso), max(parsed_iso)

        month_days = re.findall(
            r"(?<!\d)(\d{1,2})\s*월\s*(\d{1,2})\s*일",
            message,
        )
        parsed_month_days = ChatService._valid_dates(
            [(str(today.year), month, day) for month, day in month_days]
        )
        if parsed_month_days:
            return min(parsed_month_days), max(parsed_month_days)

        year_month = re.search(r"(\d{4})\s*년\s*(\d{1,2})\s*월", message)
        if year_month:
            year, month = map(int, year_month.groups())
            if 1 <= month <= 12:
                last_day = calendar.monthrange(year, month)[1]
                return date(year, month, 1), date(year, month, last_day)

        if "오늘" in message or "진행 중" in message:
            return today, today

        if "이번 주말" in message:
            days_until_saturday = (5 - today.weekday()) % 7
            start = today + timedelta(days=days_until_saturday)
            return start, start + timedelta(days=1)

        if "이번 달" in message:
            last_day = calendar.monthrange(today.year, today.month)[1]
            return date(today.year, today.month, 1), date(today.year, today.month, last_day)

        bare_month = re.search(r"(?<!\d)(\d{1,2})\s*월", message)
        if bare_month and "몇 월" not in message:
            month = int(bare_month.group(1))
            if 1 <= month <= 12:
                last_day = calendar.monthrange(today.year, month)[1]
                return date(today.year, month, 1), date(today.year, month, last_day)

        return None

    @staticmethod
    def _valid_dates(values: list[tuple[str, str, str]]) -> list[date]:
        parsed: list[date] = []
        for year, month, day in values:
            try:
                parsed.append(date(int(year), int(month), int(day)))
            except ValueError:
                continue
        return parsed

    @staticmethod
    def _format_date(value: date) -> str:
        return f"{value.year}년 {value.month}월 {value.day}일"

    @classmethod
    def _format_date_range(cls, start: date, end: date) -> str:
        if start == end:
            return cls._format_date(start)
        return f"{cls._format_date(start)}부터 {cls._format_date(end)}까지"

    @classmethod
    def _format_event_period(cls, start: str, end: str) -> str:
        try:
            start_date = datetime.strptime(start, "%Y%m%d").date()
            end_date = datetime.strptime(end, "%Y%m%d").date()
        except (TypeError, ValueError):
            return "행사 기간 정보 없음"
        return cls._format_date_range(start_date, end_date)

    @staticmethod
    def _results_from_tool(tool_name: str | None, result: Any | None) -> list[ChatResult]:
        if not isinstance(result, dict):
            return []
        items = result.get("items", [])
        if tool_name in {"search_tour_contents", "search_nearby_contents"}:
            return [
                ChatResult(
                    content_id=item.get("contentId"),
                    type=item.get("contentTypeName", "관광 콘텐츠"),
                    title=item.get("title", ""),
                    address=item.get("address", ""),
                    image_url=item.get("thumbnailUrl", ""),
                    event_start_date=item.get("eventStartDate", ""),
                    event_end_date=item.get("eventEndDate", ""),
                    event_place=item.get("eventPlace", ""),
                )
                for item in items
            ]
        if tool_name == "search_community_posts":
            return [
                ChatResult(
                    post_id=item.get("id"),
                    type="커뮤니티",
                    title=item.get("title", ""),
                )
                for item in items
            ]
        return []

    @staticmethod
    def _intent_from_tool(tool_name: str | None) -> str:
        return {
            "search_tour_contents": "TOUR_CONTENT_SEARCH",
            "search_nearby_contents": "NEARBY_CONTENT_SEARCH",
            "search_community_posts": "COMMUNITY_SEARCH",
            "get_tour_content": "TOUR_CONTENT_DETAIL",
            "get_data_source": "DATA_SOURCE",
        }.get(tool_name, "GENERAL")
