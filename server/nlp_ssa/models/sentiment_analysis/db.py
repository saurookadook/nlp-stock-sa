import uuid
from sqlalchemy import Float, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from constants import SentimentEnum
from db import Base
from models.mixins import TimestampsMixinDB


SENTIMENT_ENUM = postgresql.ENUM(
    SentimentEnum,
    values_callable=lambda e: [x.value for x in e],
    name="sentiments",
    metadata=Base.metadata,
)

OUTPUT_SERVER_DEFAULT = '{"compound":0,"neg":0,"neu":0,"pos":0}'


class OutputColumn:
    compound: Mapped[float]
    neg: Mapped[float]
    neu: Mapped[float]
    pos: Mapped[float]


class SentimentAnalysisDB(Base, TimestampsMixinDB):
    __tablename__ = "sentiment_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    quote_stock_symbol: Mapped[str] = mapped_column(
        ForeignKey("stocks.quote_stock_symbol"), nullable=False
    )  # reuse as slug?
    source_group_id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), nullable=False
    )
    output: Mapped[OutputColumn] = mapped_column(
        postgresql.JSONB,
        default={"compound": 0, "neg": 0, "neu": 0, "pos": 0},
        server_default=OUTPUT_SERVER_DEFAULT,
        nullable=False,
    )
    score: Mapped[float] = mapped_column(Float)
    sentiment: Mapped[SentimentEnum] = mapped_column(
        SENTIMENT_ENUM,
        server_default=SentimentEnum.NEUTRAL.value,
        default=SentimentEnum.NEUTRAL,
        nullable=False,
    )
    # TODO: add 'output' column
