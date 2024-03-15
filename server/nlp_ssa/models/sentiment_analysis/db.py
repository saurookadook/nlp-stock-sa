import arrow
import enum
from sqlalchemy import Column, ForeignKey, Float, String, Text
from sqlalchemy.dialects import postgresql

from db import Base
from models.mixins import TimestampsMixin
from models.sentiment_analysis import SentimentEnum


SENTIMENT_ENUM = postgresql.ENUM(
    SentimentEnum,
    values_callable=lambda e: [x.value for x in e],
    name="sentiments",
    metadata=Base.metadata,
)


class SentimentAnalysisDB(Base, TimestampsMixin):
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
