from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    dataset_name: Mapped[str] = mapped_column(String(200), nullable=False)
    api_name: Mapped[str] = mapped_column(String(100), nullable=False)
    region: Mapped[str] = mapped_column(String(50), nullable=False)
    license_name: Mapped[str] = mapped_column(String(100), nullable=False)
    commercial_use: Mapped[bool] = mapped_column(Boolean, nullable=False)
    modification_allowed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    source_url: Mapped[str] = mapped_column(Text, nullable=False)
    collected_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    attribution_text: Mapped[str] = mapped_column(Text, nullable=False)
