from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

from models.mixins import TimestampsMixin


class Stock(BaseModel, TimestampsMixin):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    quote_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    full_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    exchange_name: Optional[str]
