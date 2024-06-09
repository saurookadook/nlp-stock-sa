from sqlalchemy import Float, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID

from constants.db_types import SentimentEnum, SentimentEnumDB
from db import Base
from models.mixins import TimestampsMixinDB


OUTPUT_SERVER_DEFAULT = '{"compound":0,"neg":0,"neu":0,"pos":0}'


class OutputColumn:
    compound: Mapped[float]
    neg: Mapped[float]
    neu: Mapped[float]
    pos: Mapped[float]


class SentimentAnalysisDB(Base, TimestampsMixinDB):
    __tablename__ = "sentiment_analyses"

    id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    quote_stock_symbol: Mapped[str] = mapped_column(
        ForeignKey("stocks.quote_stock_symbol"), nullable=False
    )  # reuse as slug?
    # TODO: should have source relationship...?
    source_group_id: Mapped[UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), nullable=False
    )
    source_id: Mapped[UUID] = mapped_column(ForeignKey("sources.id"), nullable=True)
    source: Mapped["SourceDB"] = relationship(
        back_populates="related_sentiment_analyses"
    )
    output: Mapped[OutputColumn] = mapped_column(
        postgresql.JSONB,
        default={"compound": 0, "neg": 0, "neu": 0, "pos": 0},
        server_default=OUTPUT_SERVER_DEFAULT,
        nullable=False,
    )
    score: Mapped[float] = mapped_column(Float)
    sentiment: Mapped[SentimentEnum] = mapped_column(
        SentimentEnumDB,
        server_default=SentimentEnum.NEUTRAL.value,
        default=SentimentEnum.NEUTRAL,
        nullable=False,
    )
