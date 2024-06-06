from pydantic import BaseModel, ConfigDict
from uuid import UUID

from models.mixins import TimestampsMixin
from models.sentiment_analysis import SentimentEnum


class AnalysisOutput(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    compound: float
    neg: float
    neu: float
    pos: float


class SentimentAnalysis(BaseModel, TimestampsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str
    source_group_id: UUID
    output: AnalysisOutput
    score: float
    sentiment: SentimentEnum
