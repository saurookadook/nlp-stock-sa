import arrow
import enum
from sqlalchemy import Column, ForeignKey, Float, String, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

from db import Base, ArrowDate
from models.sentiment_analysis import SentimentEnum


SENTIMENT_ENUM = postgresql.ENUM(
    SentimentEnum,
    values_callable=lambda e: [x.value for x in e],
    name="sentiments",
    metadata=Base.metadata,
)


class SentimentAnalysisDB(Base):
    __tablename__ = "sentiment_analyses"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, nullable=False)
    stock_symbol = Column(String(length=10), nullable=False)  # reuse as slug?
    score = Column(Float)
    sentiment = Column(
        SENTIMENT_ENUM,
        server_default=SentimentEnum.NEUTRAL.value,
        default=SentimentEnum.NEUTRAL,
        nullable=False,
    )
    source_group_id = Column(postgresql.UUID(as_uuid=True), nullable=False)
    created_at = Column(ArrowDate(), nullable=False, server_default=func.now())
    updated_at = Column(
        ArrowDate(), nullable=False, server_default=func.now(), onupdate=arrow.utcnow
    )
