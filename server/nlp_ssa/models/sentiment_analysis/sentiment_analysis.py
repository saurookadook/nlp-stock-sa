from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional
from uuid import UUID

from constants import SentimentEnum
from models.mixins import TimestampsMixin
from models.source import Source


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
    source_id: Annotated[Optional[UUID], Field(default_factory=lambda: None)]
    source: Annotated[Optional[Source], Field(default_factory=lambda: None)]
    output: AnalysisOutput
    score: float
    sentiment: SentimentEnum
