from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from app.api import areas, chat, contents, images, posts, sources
from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine
from app.models import DataSource


def seed_data_source() -> None:
    with SessionLocal() as db:
        if db.scalar(select(DataSource.id).limit(1)):
            return
        db.add(
            DataSource(
                provider="한국관광공사",
                dataset_name="국문 관광정보 서비스",
                api_name="TourAPI 4.0",
                region="광주_전라권",
                license_name="공공누리 제3유형",
                commercial_use=True,
                modification_allowed=False,
                source_url="https://www.data.go.kr/data/15101578/openapi.do",
                collected_at=None,
                attribution_text=(
                    "이 서비스는 한국관광공사 TourAPI 4.0 데이터를 활용하였습니다."
                ),
            )
        )
        db.commit()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_data_source()
    yield


settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(areas.router)
app.include_router(contents.router)
app.include_router(posts.router)
app.include_router(chat.router)
app.include_router(sources.router)
app.include_router(images.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
