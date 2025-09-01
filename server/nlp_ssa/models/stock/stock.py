from typing import Optional
from uuid import UUID

from models.mixins import TimestampsMixin
from utils.pydantic_helpers import BaseAppModel


class Stock(BaseAppModel, TimestampsMixin):
    id: UUID
    quote_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    full_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    exchange_name: Optional[str]
