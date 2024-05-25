import uuid
from sqlalchemy import String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

from db import Base
from models.mixins import TimestampsMixin


class StockDB(Base, TimestampsMixin):
    __tablename__ = "stocks"

    id: Mapped[uuid.UUID] = mapped_column(
        postgresql.UUID(as_uuid=True), primary_key=True, nullable=False
    )
    quote_stock_symbol: Mapped[str] = mapped_column(
        String(length=10), nullable=False, unique=True
    )
    full_stock_symbol: Mapped[str] = mapped_column(
        String(length=255), nullable=False, unique=True
    )
    exchange_name: Mapped[str] = mapped_column(String(255), nullable=True, unique=False)
