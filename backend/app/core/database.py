from collections.abc import Generator

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
connect_args = (
    {"check_same_thread": False}
    if settings.database_url.startswith("sqlite")
    else {}
)
engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


EVENT_COLUMNS: dict[str, str] = {
    "event_start_date": "VARCHAR(8) NOT NULL DEFAULT ''",
    "event_end_date": "VARCHAR(8) NOT NULL DEFAULT ''",
    "event_place": "TEXT NOT NULL DEFAULT ''",
    "playtime": "TEXT NOT NULL DEFAULT ''",
    "program": "TEXT NOT NULL DEFAULT ''",
    "subevent": "TEXT NOT NULL DEFAULT ''",
    "sponsor1": "TEXT NOT NULL DEFAULT ''",
    "sponsor1_tel": "VARCHAR(100) NOT NULL DEFAULT ''",
    "sponsor2": "TEXT NOT NULL DEFAULT ''",
    "sponsor2_tel": "VARCHAR(100) NOT NULL DEFAULT ''",
    "event_homepage": "TEXT NOT NULL DEFAULT ''",
    "booking_place": "TEXT NOT NULL DEFAULT ''",
    "age_limit": "TEXT NOT NULL DEFAULT ''",
    "festival_grade": "TEXT NOT NULL DEFAULT ''",
    "place_info": "TEXT NOT NULL DEFAULT ''",
    "spend_time_festival": "TEXT NOT NULL DEFAULT ''",
    "discount_info_festival": "TEXT NOT NULL DEFAULT ''",
    "use_time_festival": "TEXT NOT NULL DEFAULT ''",
}


def ensure_tour_content_event_columns() -> None:
    """기존 SQLite DB에도 축제 일정 컬럼을 안전하게 추가한다.

    SQLAlchemy의 create_all은 이미 존재하는 테이블에 새 컬럼을 추가하지 않으므로,
    기존 regional_tour.db를 그대로 사용하는 경우를 위해 가벼운 호환 마이그레이션을 수행한다.
    """

    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)
    if "tour_contents" not in inspector.get_table_names():
        return

    existing = {column["name"] for column in inspector.get_columns("tour_contents")}
    missing = [name for name in EVENT_COLUMNS if name not in existing]

    if missing:
        with engine.begin() as connection:
            for name in missing:
                connection.execute(
                    text(
                        f'ALTER TABLE tour_contents ADD COLUMN "{name}" '
                        f"{EVENT_COLUMNS[name]}"
                    )
                )

    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_tour_contents_event_start_date "
                "ON tour_contents (event_start_date)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_tour_contents_event_end_date "
                "ON tour_contents (event_end_date)"
            )
        )
        connection.execute(
            text(
                "CREATE INDEX IF NOT EXISTS idx_tour_content_event_period "
                "ON tour_contents (content_type_id, event_start_date, event_end_date)"
            )
        )


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
