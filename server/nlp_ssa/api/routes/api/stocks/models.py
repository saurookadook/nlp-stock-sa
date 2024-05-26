from typing import List

from models.stock import Stock
from utils.pydantic_helpers import BaseResponseModel


class StockEntry(BaseResponseModel, Stock):
    pass


class SingularStockResponse(BaseResponseModel):
    data: StockEntry


class AllStocksResponse(BaseResponseModel):
    data: List[StockEntry]
