from typing import Literal

from pydantic import Field

from app.schemas.common import CamelModel


class ChatHistoryItem(CamelModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(CamelModel):
    message: str = Field(min_length=1, max_length=1000)
    history: list[ChatHistoryItem] = Field(default_factory=list)


class ChatResult(CamelModel):
    content_id: str | None = None
    post_id: int | None = None
    type: str
    title: str
    address: str = ""
    image_url: str = ""
    event_start_date: str = ""
    event_end_date: str = ""
    event_place: str = ""


class ChatSource(CamelModel):
    provider: str = "한국관광공사"
    license: str = "공공누리 제3유형"


class ChatResponse(CamelModel):
    answer: str
    intent: str
    results: list[ChatResult] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    source: ChatSource = Field(default_factory=ChatSource)
    used_openai: bool = False
