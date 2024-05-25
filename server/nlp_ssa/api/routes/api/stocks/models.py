from typing import List

from models.stock import Stock
from utils.pydantic_helpers import BaseResponseModel


class StockEntry(BaseResponseModel, Stock):
    pass


class AllStocksResponse(BaseResponseModel):
    data: List[StockEntry]
