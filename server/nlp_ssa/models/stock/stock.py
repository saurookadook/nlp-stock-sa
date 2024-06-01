from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from utils.pydantic_helpers import SerializerArrowType


class Stock(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    full_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    exchange_name: Optional[str]
    created_at: SerializerArrowType
    updated_at: SerializerArrowType
