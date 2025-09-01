from typing import Optional
from uuid import UUID

from utils.pydantic_helpers import BaseAppModel


class Stock(BaseAppModel):
    id: UUID
    quote_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    full_stock_symbol: str = (
        ""  # TODO: for some bizarre reason, these raise errors without the default value
    )
    exchange_name: Optional[str]
