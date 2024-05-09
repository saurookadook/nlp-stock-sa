import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from db import ArrowDate, Base
from models.mixins import TimestampsMixin
from utils.pydantic_helpers import ArrowType


class ArticleDataDB(Base, TimestampsMixin):
    __tablename__ = "article_data"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    quote_stock_symbol: Mapped[str] = mapped_column(
        ForeignKey("stocks.quote_stock_symbol"), nullable=False
    )  # reuse as slug?
    source_group_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), nullable=False
    )
    source_url: Mapped[str] = mapped_column(String(2048), nullable=False)

    author: Mapped[str] = mapped_column(String, nullable=True)
    last_updated_date: Mapped[ArrowType] = mapped_column(ArrowDate(), nullable=True)
    published_date: Mapped[ArrowType] = mapped_column(ArrowDate(), nullable=True)
    raw_content: Mapped[str] = mapped_column(String(), nullable=True)
    sentence_tokens: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
