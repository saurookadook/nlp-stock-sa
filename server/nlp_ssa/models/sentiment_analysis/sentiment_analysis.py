from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Annotated, Optional
from uuid import UUID

from constants import SentimentEnum
from models.mixins import TimestampsMixin
from models.source import Source
from utils.pydantic_helpers import generic_validator_with_default


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

    @field_validator("source_id", "source")
    @classmethod
    def handle_field_defaults(cls, value, info):
        return generic_validator_with_default(cls, value, info)
