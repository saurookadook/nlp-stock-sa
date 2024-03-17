from pydantic import BaseModel
from uuid import UUID

from utils.pydantic_helpers import ArrowType


class Stock(BaseModel):
    class Config:
        orm_mode = True

        id: UUID
        quote_stock_symobol: str
        full_stock_symobol: str
        created_at: ArrowType
        updated_at: ArrowType
