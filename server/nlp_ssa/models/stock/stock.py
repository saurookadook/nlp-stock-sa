from pydantic import BaseModel, ConfigDict
from uuid import UUID

from utils.pydantic_helpers import ArrowType


class Stock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symobol: str
    full_stock_symobol: str
    created_at: ArrowType
    updated_at: ArrowType
