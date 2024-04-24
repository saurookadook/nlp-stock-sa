import uuid
from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from models.mixins import TimestampsMixin
from models.sentiment_analysis.constants import SentimentEnum


SENTIMENT_ENUM = postgresql.ENUM(
    SentimentEnum,
    values_callable=lambda e: [x.value for x in e],
    name="sentiments",
    metadata=Base.metadata,
)


class SentimentAnalysisDB(Base, TimestampsMixin):
    __tablename__ = "sentiment_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    source_group_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), nullable=False
    )
    quote_stock_symbol: Mapped[str] = mapped_column(
        String(length=10), nullable=False
    )  # reuse as slug?
    score: Mapped[float] = mapped_column(Float)
    sentiment: Mapped[SentimentEnum] = mapped_column(
        SENTIMENT_ENUM,
        server_default=SentimentEnum.NEUTRAL.value,
        default=SentimentEnum.NEUTRAL,
        nullable=False,
    )
    # TODO: add 'output' column
