from pydantic import BaseModel, ConfigDict
from uuid import UUID

from models.sentiment_analysis import SentimentEnum
from utils.pydantic_helpers import ArrowType


class SentimentAnalysis(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str
    score: float
    sentiment: SentimentEnum
    source_group_id: UUID
    created_at: ArrowType
    updated_at: ArrowType
