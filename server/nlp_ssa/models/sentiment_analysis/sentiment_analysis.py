from pydantic import BaseModel
from uuid import UUID

from models.sentiment_analysis import SentimentEnum
from utils.pydantic_helpers import ArrowType


class SentimentAnalysis(BaseModel):
    class Config:
        orm_mode = True

        id: UUID
        quote_stock_symbol: str
        score: float
        sentiment: SentimentEnum
        source_group_id: UUID
        created_at: ArrowType
        updated_at: ArrowType
