import uuid
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from models.mixins import TimestampsMixin


class ArticleDataDB(Base, TimestampsMixin):
    __tablename__ = "sentence_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    source_group_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), nullable=False
    )
    quote_stock_symbol: Mapped[str] = mapped_column(
        String(length=10), nullable=False
    )  # reuse as slug?
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    sentence_tokens: Mapped[str] = mapped_column(String(), nullable=True)
    raw_content: Mapped[str] = mapped_column(String(), nullable=True)
