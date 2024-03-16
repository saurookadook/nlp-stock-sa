from sqlalchemy import Column, String
from sqlalchemy.dialects import postgresql

from db import Base
from models.mixins import TimestampsMixin


class StockDB(Base, TimestampsMixin):
    __tablename__ = "stocks"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, nullable=False)
    quote_stock_symbol = Column(String(length=12), nullable=False, unique=True)
    fall_stock_symbol = Column(String(length=255), nullable=False, unique=True)
