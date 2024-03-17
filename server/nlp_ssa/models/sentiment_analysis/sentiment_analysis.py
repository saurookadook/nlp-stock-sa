from pydantic import BaseModel, ConfigDict
from pydantic.functional_validators import WrapValidator
from typing import Annotated
from uuid import UUID

from models.sentiment_analysis import SentimentEnum
from utils.pydantic_helpers import convert_to_arrow_instance


class SentimentAnalysis(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str
    score: float
    sentiment: SentimentEnum
    source_group_id: UUID
    created_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
    updated_at: Annotated[str, WrapValidator(convert_to_arrow_instance)]
