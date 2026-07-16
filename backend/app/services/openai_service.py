import json
from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

try:
    from openai import AsyncOpenAI
except ImportError:  # 선택 기능: SDK가 없으면 규칙 기반 fallback 사용
    AsyncOpenAI = None  # type: ignore[assignment]

from app.core.config import Settings


SYSTEM_PROMPT = """
너는 광주·전라권 관광정보 안내 챗봇이다.
반드시 도구 검색 결과와 제공 데이터만 사용해 답변한다.

축제공연행사(contentTypeId=15)에는 행사 시작일 eventStartDate와 종료일 eventEndDate가 제공될 수 있다.
두 날짜의 원본 형식은 YYYYMMDD이다. 사용자에게는 읽기 쉬운 한국어 날짜로 안내한다.
사용자가 오늘, 이번 주말, 이번 달 또는 특정 날짜의 축제를 요청하면 search_tour_contents의
query_start_date와 query_end_date에 YYYYMMDD 형식의 조회 범위를 넣는다.
행사 시작일이 조회 종료일보다 빠르거나 같고 행사 종료일이 조회 시작일보다 늦거나 같은,
즉 조회 기간과 행사 기간이 하루라도 겹치는 축제만 안내한다.

축제의 eventPlace, playtime, program, useTimeFestival 등은 값이 있을 때만 안내한다.
해당 값이 비어 있으면 추측하지 않는다. createdtime과 modifiedtime은 축제 개최일이 아니라
한국관광공사 데이터의 등록·수정 시각이다.

음식점의 메뉴, 가격, 영업시간, 모범음식점 지정 여부와 위생등급은 데이터에 없으면 추측하지 않는다.
일반 음식점 데이터를 모범음식점이라고 표현하지 않는다.
여행코스 데이터에 코스 구성 장소가 없으면 임의로 경로를 만들지 않는다.
검색 결과가 없거나 필요한 필드가 없으면 확인할 수 없다고 명확히 안내한다.
가능하면 장소명, 주소, 콘텐츠 유형과 축제의 경우 행사 기간을 포함한다.
마지막에는 '출처: 한국관광공사 TourAPI 4.0 / 라이선스: 공공누리 제3유형'을 표시한다.
""".strip()


TOOLS = [
    {
        "type": "function",
        "name": "search_tour_contents",
        "description": (
            "관광 콘텐츠를 유형, 지역, 키워드, 이미지 여부와 축제 행사 기간으로 검색한다. "
            "날짜 조건은 행사 기간과 조회 기간이 겹치는 항목을 찾는다."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "content_type_id": {"type": ["string", "null"]},
                "area_code": {"type": ["string", "null"]},
                "sigungu_code": {"type": ["string", "null"]},
                "keyword": {"type": ["string", "null"]},
                "has_image": {"type": ["boolean", "null"]},
                "query_start_date": {
                    "type": ["string", "null"],
                    "description": "축제 조회 기간 시작일(YYYYMMDD)",
                },
                "query_end_date": {
                    "type": ["string", "null"],
                    "description": "축제 조회 기간 종료일(YYYYMMDD)",
                },
                "limit": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["limit"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "search_nearby_contents",
        "description": "사용자가 제공한 위도·경도를 기준으로 반경 내 가까운 관광 콘텐츠를 검색한다.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "minimum": -90, "maximum": 90},
                "longitude": {"type": "number", "minimum": -180, "maximum": 180},
                "content_type_id": {"type": ["string", "null"]},
                "area_code": {"type": ["string", "null"]},
                "radius_km": {"type": "number", "minimum": 0.1, "maximum": 100},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["latitude", "longitude", "radius_km", "limit"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "search_community_posts",
        "description": "익명 커뮤니티 게시글을 검색한다.",
        "parameters": {
            "type": "object",
            "properties": {
                "keyword": {"type": "string"},
                "category": {"type": ["string", "null"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["keyword", "limit"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_tour_content",
        "description": "contentId로 관광 콘텐츠 상세와 축제 일정 정보를 조회한다.",
        "parameters": {
            "type": "object",
            "properties": {"content_id": {"type": "string"}},
            "required": ["content_id"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "get_data_source",
        "description": "데이터 출처와 라이선스를 조회한다.",
        "parameters": {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
    },
]


class OpenAIService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = (
            AsyncOpenAI(api_key=settings.openai_api_key)
            if settings.openai_api_key and AsyncOpenAI is not None
            else None
        )

    @property
    def enabled(self) -> bool:
        return self.client is not None

    async def answer(
        self,
        *,
        message: str,
        history: list[dict[str, str]],
        tool_handlers: dict[str, Callable[..., Awaitable[Any]]],
    ) -> tuple[str, str | None, Any | None]:
        if not self.client:
            raise RuntimeError("OPENAI_API_KEY가 설정되지 않았습니다.")

        conversation: list[Any] = [
            {"role": item["role"], "content": item["content"]}
            for item in history[-8:]
        ]
        conversation.append({"role": "user", "content": message})

        today = datetime.now(ZoneInfo("Asia/Seoul")).date().isoformat()
        instructions = f"{SYSTEM_PROMPT}\n현재 한국 날짜는 {today}이다."

        last_tool_name: str | None = None
        last_tool_result: Any | None = None

        for _ in range(4):
            response = await self.client.responses.create(
                model=self.settings.openai_model,
                instructions=instructions,
                input=conversation,
                tools=TOOLS,
                store=False,
            )
            conversation.extend(response.output)
            calls = [
                item for item in response.output
                if getattr(item, "type", None) == "function_call"
            ]
            if not calls:
                return response.output_text, last_tool_name, last_tool_result

            for call in calls:
                arguments = json.loads(call.arguments or "{}")
                handler = tool_handlers.get(call.name)
                if not handler:
                    result = {"error": f"지원하지 않는 도구: {call.name}"}
                else:
                    result = await handler(**arguments)
                last_tool_name = call.name
                last_tool_result = result
                conversation.append(
                    {
                        "type": "function_call_output",
                        "call_id": call.call_id,
                        "output": json.dumps(result, ensure_ascii=False),
                    }
                )

        raise RuntimeError("도구 호출 반복 한도를 초과했습니다.")
